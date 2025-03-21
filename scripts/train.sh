#!/bin/bash

export CUDA_VISIBLE_DEVICES="0,1,2,3,4,5,6,7"

LOG_DIR=../logs/sft
mkdir -p $LOG_DIR

N_EPOCH=3
WARMUP_RATIO=0.03
GRADIENT_ACCUMULATION_STEPS=8
LR=1e-5

MODEL_NAME=meta-llama/Meta-Llama-3-8B

DATA_PATHS=(
    data_path_here
)
for DATA_PATH in ${DATA_PATHS[@]}; do
    echo ${JOB_NAME}
    echo ${DATA_PATH}
    START_TIME=`date +%Y%m%d-%H:%M:%S`
    LOG_FILE=${LOG_DIR}/${START_TIME}_${JOB_NAME}.log
    bash LLaMA-Factory/sh/launch_sft.sh $MODEL_NAME $DATA_PATH $LR $WARMUP_RATIO $GRADIENT_ACCUMULATION_STEPS $N_EPOCH >> ${LOG_FILE}
done
