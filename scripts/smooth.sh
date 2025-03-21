#!/bin/bash

N_PROCESS=8
DATA_PATH=evaluation/outputs/meta-llama/Meta-Llama-3-8B/math_eval/train_cot-meta-math/math/train_cot-meta-math_-1_seed0_t0.7_s0_e-1_gpt-4o-mini_error-step_gpt-4o-mini_corrected_filtered.jsonl
MODEL_NAME_OR_PATH=gpt-4o
MAX_MODEL_LEN=32768
LOAD_KEY=corrected_solution

python smooth.py \
    --data_path ${DATA_PATH} \
    --model_name ${MODEL_NAME_OR_PATH} \
    --n_process ${N_PROCESS} \
    --max_model_len ${MAX_MODEL_LEN} \
    --load_key ${LOAD_KEY} \
    --resume
