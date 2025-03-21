#!/bin/bash

N_PROCESS=8
DATA_PATH=evaluation/outputs/meta-llama/Meta-Llama-3-8B/math_eval/train_cot-meta-math/math/train_cot-meta-math_-1_seed0_t0.7_s0_e-1_gpt-4o-mini_error-step.jsonl
MODEL_NAME_OR_PATH=gpt-4o
MAX_MODEL_LEN=32768

python correct.py \
    --data_path $DATA_PATH \
    --model_name $MODEL_NAME_OR_PATH \
    --n_process $N_PROCESS \
    --max_model_len $MAX_MODEL_LEN \
    --resume \
    --stop_at_first_error
