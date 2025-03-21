# Licensed under The MIT License [see LICENSE for details]

import os
import os.path as osp
import re
from concurrent.futures import TimeoutError
from datetime import datetime
from time import sleep
from typing import List

from dotenv import load_dotenv
from pebble import ProcessPool
from tqdm import tqdm
from vllm import LLM, SamplingParams


class OpenAILLM:
    def __init__(
        self,
        model_name="gpt-4o-mini-2024-07-18",
        api_key_file_path="~/dot_env/openai.env",
    ):
        from openai import OpenAI

        self.model_name = model_name
        load_dotenv(osp.expanduser(api_key_file_path))

        self.client = OpenAI()
        self.client.base_url = os.getenv("OPENAI_API_BASE")
        keys = os.getenv("OPENAI_API_KEY")
        self.client.api_key = keys.split(",")[0]

    def __call__(
        self,
        prompts: List[str],
        system_prompt=None,
        temperature=0.7,
        top_p=1.0,
        max_tokens=4096,
        seed=None,
        max_num_retries=2,
        return_full=False,
        stop: List[str] = [],
    ) -> str:
        prompt_list = prompts
        if isinstance(prompts, str):
            prompt_list = [prompts]

        outputs = []
        for prompt in tqdm(prompt_list, desc="Processing prompts", unit="prompt"):
            output = self.generate(
                prompt,
                system_prompt,
                temperature,
                top_p,
                max_tokens,
                seed,
                max_num_retries,
                return_full,
                stop,
            )
            outputs.append(output)
        if isinstance(prompts, str):
            return outputs[0]
        return outputs

    def generate(
        self,
        prompt,
        system_prompt=None,
        temperature=0.7,
        top_p=1.0,
        max_tokens=4096,
        seed=42,
        max_num_retries=2,
        return_full=False,
        stop: List[str] = [],
        idx=None,
    ) -> str:
        if system_prompt is not None:
            messages = [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ]
        else:
            messages = [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]

        retry = 0
        while retry < max_num_retries:
            try:
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=temperature,
                    top_p=top_p,
                    max_tokens=max_tokens,
                    seed=seed,
                    stop=stop,
                )
                content = completion.choices[0].message.content
                if not return_full:
                    if idx is not None:
                        return idx, content
                    else:
                        return content

                ret_dict = {
                    "prompt": prompt,
                    "system_prompt": system_prompt,
                    "model_name": self.model_name,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "response": content,
                    "response_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                return ret_dict

            except Exception as e:
                retry += 1
                sleep(5)
                print(f"Error: {e}", flush=True)

        raise RuntimeError(
            "Calling OpenAI failed after retrying for " f"{retry} times."
        )


def extract_error_type(response):
    legal_error_types = [
        "calculation_error",
        "counting_error",
        "question_understanding_error",
        "referencing_context_value_error",
        "referencing_previous_step_value_error",
        "unit_conversion_error",
        "operator_error",
        "missing_step",
        "confusing_formula_error",
        "confusing_concept_error",
        "adding_irrelevant_information",
        "nonsense_output_error",
    ]
    strip_tokens = [
        "`",
        "'",
        '"',
        "*",
    ]
    valid = True
    correct = False
    error_type = ""
    start_phrase = "The solution is"
    start_index = response.find(start_phrase)

    if start_index != -1:
        start_index += len(start_phrase)
        words_after_phrase = response[start_index:].split()
        if words_after_phrase:
            next_word = words_after_phrase[0]
            if "incorrect" in next_word:
                start_index1 = response.find("the wrong type is ")
                if start_index1 == -1:
                    valid = False
                else:
                    error_type_start = start_index1 + len("the wrong type is ")
                    error_type_end = response.find(".", error_type_start)
                    if error_type_end == -1:
                        error_type_end = len(response)
                    error_type_candidate = response[
                        error_type_start:error_type_end
                    ].strip()
                    for token in strip_tokens:
                        error_type_candidate = error_type_candidate.strip(token)
                    if error_type_candidate in legal_error_types:
                        error_type = error_type_candidate
                    else:
                        valid = False
            else:
                valid = False
                correct = True
        else:
            valid = False
    else:
        valid = False
    if not valid:
        for et in legal_error_types:
            if et in response:
                error_type = et
                correct = False
                valid = True
    return valid, correct, error_type


def extract_error_step(response):
    valid = True
    correct = False
    error_step = 1
    start_phrase = "The solution is"
    start_index = response.find(start_phrase)

    if start_index != -1:
        start_index += len(start_phrase)
        words_after_phrase = response[start_index:].split()
        if words_after_phrase:
            next_word = words_after_phrase[0]
            if "incorrect" in next_word:
                match = re.search(r"first wrong step is step (\d+)", response)
                if match:
                    error_step = int(match.group(1))
                else:
                    valid = False
            else:
                valid = False
                correct = True
        else:
            valid = False
    else:
        valid = False
    return valid, correct, error_step
