#!/bin/bash

cd "$(dirname "$0")/.."

DATA_NAME=$1
PROMPT_TYPE=$2
MODEL_NAME_OR_PATH=$3

SPLIT="test"
TEMPERATURE=0
N_SAMPLEING=1
SEED=0
OUTPUT_DIR=${MODEL_NAME_OR_PATH}/math_eval/test_${PROMPT_TYPE}_zero-shot
NUM_TEST_SAMPLE=-1

TOKENIZERS_PARALLELISM=false \
python3 -u math_eval.py \
    --model_name_or_path ${MODEL_NAME_OR_PATH} \
    --data_name ${DATA_NAME} \
    --output_dir ${OUTPUT_DIR} \
    --split ${SPLIT} \
    --prompt_type ${PROMPT_TYPE} \
    --num_test_sample ${NUM_TEST_SAMPLE} \
    --seed ${SEED} \
    --temperature ${TEMPERATURE} \
    --n_sampling ${N_SAMPLEING} \
    --top_p 1 \
    --start 0 \
    --end -1 \
    --use_vllm \
    --save_outputs \
    --num_shots 0
