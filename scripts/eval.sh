#!/bin/bash

export CUDA_VISIBLE_DEVICES=0

tasks=("gsm8k" "math" "deepmind_math" "college_math")
tasks_ood=("mawps" "svamp" "asdiv")
prompt_type="cot-meta-math"
MODELS=(
    sft-models/meta-llama/Meta-Llama-3-8B/math_data/LEMMA/cot-meta-math/gsm8k_math_train_Base_lr1e-5_warm0.03_gas8_epoch3/checkpoint-1041
)

for model_name_or_path in ${MODELS[@]}; do
    for task in ${tasks[@]}; do
        bash evaluation/sh/eval_zero-shot.sh ${task} ${prompt_type} ${model_name_or_path}
    done
    for task in ${tasks_ood[@]}; do
        bash evaluation/sh/eval_few-shot.sh ${task} ${prompt_type} ${model_name_or_path}
    done
done

echo done
