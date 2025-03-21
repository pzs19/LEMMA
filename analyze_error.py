# Licensed under The MIT License [see LICENSE for details]

import argparse
import json
import multiprocessing
import os
from datetime import datetime

from tqdm import tqdm

from _utils import OpenAILLM, extract_error_step, extract_error_type

LOG_STEP = 100


def get_qa_pair(data, dataset_type):
    output_format = " Please also give your final number in the format of 'The answer is: [your answer]'"
    if dataset_type == "gsm8k":
        question = data["question"] + output_format
        answer = data["answer"].replace("####", "The answer is:")
    elif dataset_type == "math":
        question = data["question"] + output_format
        answer = data["solution"] + f" The answer is: {data['gt']}"
    return question, answer


def error_step(data, question, answer, llm, prompt_template, spliter):
    prompts = []
    false_pred_inds = []
    data["error_step"] = ["/"] * len(data["code"])
    data["error_step_response"] = ["/"] * len(data["code"])
    data["steps"] = [code.split(spliter) for code in data["code"]]
    for pred_idx, steps in enumerate(data["steps"]):
        if data["score"][pred_idx]:
            data["error_step"][pred_idx] = "/"
            data["error_step_response"][pred_idx] = "/"
            continue
        pred = ".\n".join([f"step {i+1}: {step}" for i, step in enumerate(steps)])
        p = prompt_template.format(
            question=question, gt_solution=answer, pred_solution=pred
        )
        prompts.append(p)
        false_pred_inds.append(pred_idx)

    outputs = llm(prompts, stop=["\n\n[", "\n\n#", "###", "[Question]"])
    for pred_idx, output in zip(false_pred_inds, outputs):
        data["error_step_response"][pred_idx] = output
        valid, correct, error_step = extract_error_step(output)
        if valid:
            data["error_step"][pred_idx] = error_step
        else:
            if not correct:
                data["error_step"][pred_idx] = "invalid_response"
            else:
                data["error_step"][pred_idx] = "correct"
    return data


def error_type(data, question, answer, llm, prompt_template):
    prompts = []
    false_pred_inds = []
    data["error_type"] = ["/"] * len(data["code"])
    data["error_type_response"] = ["/"] * len(data["code"])
    for pred_idx, pred in enumerate(data["code"]):
        if data["score"][pred_idx]:
            data["error_type"][pred_idx] = "/"
            data["error_type_response"][pred_idx] = "/"
            continue
        p = prompt_template.format(
            question=question, gt_solution=answer, pred_solution=pred
        )
        prompts.append(p)
        false_pred_inds.append(pred_idx)

    outputs = llm(prompts, stop=["\n\n[", "\n\n#", "###", "[Question]"])
    for pred_idx, output, prompt in zip(false_pred_inds, outputs, prompts):
        data["error_type_response"][pred_idx] = output
        valid, correct, error_type = extract_error_type(output)
        if valid:
            data["error_type"][pred_idx] = error_type
        else:
            if not correct:
                data["error_type"][pred_idx] = "invalid_response"
            else:
                data["error_type"][pred_idx] = "correct"
    return data


def worker(
    process_idx,
    data_chunk,
    dataset_type,
    task,
    prompt_template,
    save_path=None,
    llm=None,
    model_name=None,
    max_model_len=32768,
):
    log_path = save_path.replace(".jsonl", ".log")

    spliter = ". " if dataset_type == "gsm8k" else ".\n"
    for data_idx, data in enumerate(tqdm(data_chunk, desc=f"Process {process_idx}:")):
        question, answer = get_qa_pair(data, dataset_type)

        if task == "error-step":
            data = error_step(data, question, answer, llm, prompt_template, spliter)
        elif task == "error-type":
            data = error_type(data, question, answer, llm, prompt_template)
        else:
            raise NotImplementedError()

        if data_idx % LOG_STEP == 0:
            with open(log_path, "a", encoding="utf-8") as log_file:
                for pred_idx in range(len(data[task.replace("-", "_")])):
                    if data[task.replace("-", "_")][pred_idx] != "/":
                        res = data[task.replace("-", "_")][pred_idx]
                        res_explain = data[f'{task.replace("-", "_")}_response'][
                            pred_idx
                        ]
                        content = f"[Sample {data['idx']}]\n\n"
                        content += f"[Question]\n{question}\n\n"
                        content += f"[Ground-truth Solution]\n{answer}\n\n"
                        content += f"[Proposed Solution]\n{data['code'][pred_idx]}\n\n"
                        content += f"[{task.upper()}]\n{res}\n\n"
                        content += f"[Explanation]:{res_explain}\n\n"
                        content += f"{'='*100}\n\n"
                        log_file.write(content)

        with open(save_path, "a", encoding="utf-8") as file:
            file.write(json.dumps(data, ensure_ascii=False) + "\n")


def load_processed(log_dir, save_fname, task, n_process=8):
    results = {}
    for i in range(n_process):
        load_path = os.path.join(log_dir, f"{save_fname}_process{i}.jsonl")
        if os.path.exists(load_path):
            with open(load_path, "r", encoding="utf-8") as infile:
                for line in infile:
                    try:
                        result = json.loads(line)
                        if task.replace("-", "_") in result:
                            results[result["idx"]] = result
                    except Exception:
                        print(f"invalid line: {line}")
    results = sorted(list(results.values()), key=lambda x: x["idx"])
    res_chunks = [results[i::n_process] for i in range(n_process)]
    for i in range(n_process):
        with open(
            os.path.join(log_dir, f"{save_fname}_process{i}.jsonl"),
            "w",
            encoding="utf-8",
        ) as outfile:
            for result in res_chunks[i]:
                outfile.write(json.dumps(result, ensure_ascii=False) + "\n")
    return results


def filter_processed(dataset, results):
    processed_indices = set()
    for result in results:
        processed_indices.add(result["idx"])
    remain_dataset = []
    for data in dataset:
        if data["idx"] not in processed_indices:
            remain_dataset.append(data)
    return remain_dataset


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_process", type=int, default=1)
    parser.add_argument("--rank", type=int, default=-1)
    parser.add_argument("--model_name", type=str, default="gpt-4o")
    parser.add_argument("--data_path", type=str, required=True)
    parser.add_argument("--max_model_len", type=int, default=32768)
    parser.add_argument("--task", type=str, default="error-step")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dryrun", action="store_true")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=-1)
    parser.add_argument("--merge_only", action="store_true")
    args = parser.parse_args()

    data_dir = os.path.dirname(args.data_path)
    save_dir = data_dir
    log_dir = os.path.join(save_dir, "logs")
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    dataset_type = os.path.basename(data_dir)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    data_fname = os.path.splitext(os.path.basename(args.data_path))[0]
    save_fname = f"{data_fname}_{args.model_name.replace('/', '-')}_{args.task}"
    save_path = os.path.join(save_dir, f"{save_fname}.jsonl")

    dataset = []
    with open(args.data_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                data = json.loads(line)
                dataset.append(data)
            except Exception:
                print(f"invalid line: {line}")
    if args.resume:
        processed_results = load_processed(
            log_dir, save_fname, args.task, args.n_process
        )
        dataset = filter_processed(dataset, processed_results)
        print(f"remain {len(dataset)} samples")
        dataset = dataset[: args.n_process * 2]

    if len(dataset) > 0:
        llm = OpenAILLM(args.model_name)
        with open(f"prompts/{args.task.replace('-', '_')}_few_shot.md", "r") as file:
            prompt_template = file.read()
        print(prompt_template)

        processes = []
        data_chunks = [dataset[i :: args.n_process] for i in range(args.n_process)]
        for proc_idx, data_chunk in enumerate(data_chunks):
            if args.rank != -1 and proc_idx != args.rank:
                continue
            save_path_this_proc = os.path.join(
                log_dir, f"{save_fname}_process{proc_idx}.jsonl"
            )
            p = multiprocessing.Process(
                target=worker,
                args=(
                    proc_idx,
                    data_chunk,
                    dataset_type,
                    args.task,
                    prompt_template,
                    save_path_this_proc,
                    llm,
                    args.model_name,
                    args.max_model_len,
                ),
            )
            p.start()
            processes.append(p)
        for p in processes:
            p.join()

    results = load_processed(log_dir, save_fname, args.task, args.n_process)
    with open(save_path, "w") as outfile:
        for res in results:
            try:
                outfile.write(json.dumps(res, ensure_ascii=False) + "\n")
            except Exception:
                print(f"invalid result: {res}")
