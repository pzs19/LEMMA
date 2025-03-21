# Licensed under The MIT License [see LICENSE for details]

import argparse
import json
import multiprocessing
import os
import sys
from collections import defaultdict
from concurrent.futures import TimeoutError

from pebble import ProcessPool
from tqdm import tqdm

from _utils import OpenAILLM

sys.path.append("evaluation")
from parser import extract_answer, strip_string

from grader import math_equal


def get_qa_pair(data, dataset_type):
    output_format = " Please also give your final number in the format of 'The answer is: [your answer]'"
    if dataset_type == "gsm8k":
        question = data["question"] + output_format
        answer = data["answer"].replace("####", "The answer is:")
    elif dataset_type == "math":
        question = data["question"] + output_format
        answer = data["solution"] + f" The answer is: {data['gt']}"
    return question, answer


def worker(
    process_idx,
    data_chunk,
    dataset_type,
    prompt_template,
    examples,
    stop_at_first_error=False,
    required_keys=None,
    save_key="corrected_solution",
    save_path=None,
    llm=None,
    model_name=None,
    max_model_len=32768,
):
    spliter = ". " if dataset_type == "gsm8k" else ".\n"
    log_path = save_path.replace(".jsonl", ".log")
    for data_idx, data in enumerate(tqdm(data_chunk, desc=f"Process {process_idx}:")):
        question, answer = get_qa_pair(data, dataset_type)

        true_inds = []
        false_inds = []
        for pred_idx in range(len(data["score"])):
            if (
                data["score"][pred_idx]
                or (
                    "error_type" in data
                    and data["error_type"][pred_idx] in ["correct", "/"]
                )
                or (
                    "error_step" in data
                    and data["error_step"][pred_idx] in ["correct", "/"]
                )
            ):
                true_inds.append(pred_idx)
            else:
                if args.stop_at_first_error:
                    try:
                        error_step = int(data["error_step"][pred_idx])
                        assert error_step >= 0 and error_step <= len(
                            data["steps"][pred_idx]
                        )
                    except Exception:
                        print(
                            f"invalid error_step: {data['error_step'][pred_idx]}, do not correct."
                        )
                        continue
                false_inds.append(pred_idx)
        if len(false_inds) == 0:
            print(f"{data_idx} all correct, continue.")
            continue

        new_data = defaultdict(list)
        for false_idx in false_inds:
            false_pred = data["code"][false_idx]
            if false_pred == "/":
                continue
            if stop_at_first_error:
                assert "error_step" in data and "steps" in data
                steps = data["steps"][false_idx]
                try:
                    error_step = int(data["error_step"][false_idx])
                except Exception:
                    print(
                        f"invalid error_step: {data['error_step'][false_idx]}, using full steps."
                    )
                    error_step = len(steps)
                false_pred = spliter.join(steps[: min(error_step, len(steps))])

            new_data["false_inds"].append(false_idx)
            new_data["false_preds"].append(false_pred)
            p = prompt_template.format(
                question=question,
                gt_solution=answer,
                pred_solution=false_pred,
                examples=examples,
            )
            new_data["prompts"].append(p)

        data[save_key] = ["/"] * len(data["code"])
        outputs = llm(new_data["prompts"])
        assert len(outputs) == len(new_data["prompts"])
        for i in range(len(outputs)):
            pred_idx = new_data["false_inds"][i]
            data[save_key][pred_idx] = outputs[i].strip()

        with open(log_path, "a", encoding="utf-8") as log_file:
            for pred_idx in range(len(data[save_key])):
                if data[save_key][pred_idx] != "/":
                    log_content = f"[Sample {data['idx']}]\n\n"
                    log_content += f"[Question]\n{question}\n\n"
                    log_content += f"[Ground-truth Solution]\n{answer}\n\n"
                    log_content += f"[False Solution]\n{data['code'][pred_idx]}\n\n"
                    log_content += (
                        f"[Corrected Solution]\n{data[save_key][pred_idx]}\n\n"
                    )
                    log_content += f"{'='*100}\n\n"
                    log_file.write(log_content)

        if required_keys is not None:
            new_data = {}
            for key in required_keys:
                if key in data:
                    new_data[key] = data[key]
            data = new_data
        with open(save_path, "a", encoding="utf-8") as file:
            file.write(json.dumps(data, ensure_ascii=False) + "\n")


def filter_sample(sample, save_key):
    for i, solution in enumerate(sample[save_key]):
        if solution != "/":
            pred = extract_answer(solution, dataset_type)
            pred = strip_string(pred, skip_unit=False)
            if not math_equal(pred, sample["gt"]):
                sample[save_key][i] = "/"
    return sample


def filter_results(results, save_key):
    results_filtered = []
    with ProcessPool(max_workers=32) as pool:
        save_keys = [save_key] * len(results)
        future = pool.map(filter_sample, results, save_keys, timeout=10)
        iterator = future.result()
        with tqdm(total=len(results), desc="Filter") as progress_bar:
            while True:
                try:
                    result = next(iterator)
                    if result[save_key].count("/") < len(result[save_key]) or result[
                        "score"
                    ].count(True) == len(result["score"]):
                        results_filtered.append(result)
                except StopIteration:
                    break
                except TimeoutError as error:
                    print(error)
                except Exception as error:
                    print(error.traceback)
                    exit()
                progress_bar.update(1)
    return results_filtered


def load_processed(log_dir, save_fname, save_key, n_process=8):
    results = []
    for i in range(n_process):
        load_path = os.path.join(log_dir, f"{save_fname}_process{i}.jsonl")
        if os.path.exists(load_path):
            with open(load_path, "r", encoding="utf-8") as infile:
                for line in infile:
                    try:
                        result = json.loads(line)
                        if save_key in result:
                            results.append(result)
                    except Exception:
                        print(f"invalid line: {line}")
    filtered_results = filter_results(results, save_key)
    unique_results = list(
        {result["idx"]: result for result in filtered_results}.values()
    )
    sorted_results = sorted(unique_results, key=lambda x: x["idx"])
    res_chunks = [sorted_results[i::n_process] for i in range(n_process)]
    for i in range(n_process):
        with open(
            os.path.join(log_dir, f"{save_fname}_process{i}.jsonl"),
            "w",
            encoding="utf-8",
        ) as outfile:
            for result in res_chunks[i]:
                outfile.write(json.dumps(result, ensure_ascii=False) + "\n")
    return sorted_results


def filter_processed(dataset, results):
    processed_indices = set()
    for result in results:
        processed_indices.add(result["idx"])
    remain_dataset = []
    for data in dataset:
        if data["idx"] not in processed_indices:
            remain_dataset.append(data)
    return remain_dataset


def count_valid_cot(results, save_key):
    cnt = 0
    for result in results:
        for solution in result[save_key]:
            if solution != "/":
                cnt += 1
    return cnt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_process", type=int, default=1)
    parser.add_argument("--model_name", type=str, default="gpt-4o")
    parser.add_argument("--data_path", type=str, required=True)
    parser.add_argument("--stop_at_first_error", action="store_true")
    parser.add_argument("--max_model_len", type=int, default=32768)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--save_key", type=str, default="corrected_solution")
    args = parser.parse_args()

    required_keys = [
        "idx",
        "question",
        "answer",
        "solution",
        "gt",
        "code",
        "score",
        "error_step",
        "error_type",
        "steps",
        args.save_key,
    ]
    data_dir = os.path.dirname(args.data_path)
    data_fname = os.path.basename(args.data_path)
    save_dir = data_dir
    log_dir = os.path.join(save_dir, "logs")
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    dataset_type = os.path.basename(data_dir)
    data_fname = os.path.splitext(os.path.basename(args.data_path))[0]
    save_fname = f"{data_fname}_{args.model_name.replace('/', '-')}_corrected"
    save_path = os.path.join(save_dir, f"{save_fname}.jsonl")

    dataset = []
    with open(args.data_path, "r") as file:
        for line in file:
            try:
                data = json.loads(line)
                dataset.append(data)
            except Exception:
                print(f"invalid line: {line}")
    if args.resume:
        processed_dataset = load_processed(
            log_dir, save_fname, args.save_key, args.n_process
        )
        dataset = filter_processed(dataset, processed_dataset)
        print(f"Remain {len(dataset)} samples")

    if len(dataset) > 0:
        llm = OpenAILLM(args.model_name) if "gpt-" in args.model_name else None
        with open(f"prompts/correct.md", "r", encoding="utf-8") as file:
            prompt_template = file.read()
        with open(
            f"prompts/examples/correct_{dataset_type}.md", "r", encoding="utf-8"
        ) as file:
            examples = file.read()
        print(prompt_template)

        processes = []
        data_chunks = [dataset[i :: args.n_process] for i in range(args.n_process)]
        for proc_idx, data_chunk in enumerate(data_chunks):
            save_path_this_process = os.path.join(
                log_dir, f"{save_fname}_process{proc_idx}.jsonl"
            )
            p = multiprocessing.Process(
                target=worker,
                args=(
                    proc_idx,
                    data_chunk,
                    dataset_type,
                    prompt_template,
                    examples,
                    args.stop_at_first_error,
                    required_keys,
                    args.save_key,
                    save_path_this_process,
                    llm,
                    args.model_name,
                    args.max_model_len,
                ),
            )
            p.start()
            processes.append(p)
        for p in processes:
            p.join()

    results = load_processed(log_dir, save_fname, args.save_key, args.n_process)
    print(
        f"Sample num: {len(results)}, Valid COT num: {count_valid_cot(results, args.save_key)}"
    )
    with open(save_path.replace(".jsonl", "_filtered.jsonl"), "w") as outfile:
        for res in results:
            try:
                outfile.write(json.dumps(res, ensure_ascii=False) + "\n")
            except Exception:
                print(f"invalid result: {res}")
