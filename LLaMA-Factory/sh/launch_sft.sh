#!/bin/bash

cd "$(dirname "$0")/.."

MODEL_NAME=$1
DATA_PATH=$2
LR=$3
WARMUP_RATIO=$4
GRADIENT_ACCUMULATION_STEPS=$5
N_EPOCH=$6

SAVE_LIMIT=1
PER_GPU_BATCH_SIZE=4
template="default"
base_model_name=${MODEL_NAME}

echo "Runing on: $(hostname)"
echo "SLURM ID: $SLURM_JOB_ID"
echo "MODEL_NAME: ${MODEL_NAME}"
echo "DATA_PATH: ${DATA_PATH}"
echo "LR: ${LR}"
echo "WARMUP_RATIO: ${WARMUP_RATIO}"
echo "GRADIENT_ACCUMULATION_STEPS: ${GRADIENT_ACCUMULATION_STEPS}"
echo "N_EPOCH: ${N_EPOCH}"

export ds_config="examples/deepspeed/ds_z2_config.json"

llamafactory-cli train \
    --stage sft \
    --do_train True \
    --model_name_or_path ${base_model_name} \
    --preprocessing_num_workers 16 \
    --finetuning_type full \
    --template ${template} \
    --flash_attn fa2 \
    --dataset_dir data \
    --dataset ${DATA_PATH} \
    --cutoff_len 4096 \
    --learning_rate ${LR} \
    --warmup_ratio ${WARMUP_RATIO} \
    --num_train_epochs ${N_EPOCH} \
    --max_samples 1000000 \
    --per_device_train_batch_size ${PER_GPU_BATCH_SIZE} \
    --gradient_accumulation_steps ${GRADIENT_ACCUMULATION_STEPS} \
    --lr_scheduler_type cosine \
    --max_grad_norm 1.0 \
    --logging_steps 5 \
    --save_strategy epoch \
    --save_steps -1 \
    --save_total_limit $SAVE_LIMIT \
    --warmup_steps 0 \
    --optim adamw_torch \
    --packing False \
    --report_to none \
    --output_dir sft-models/${base_model_name}/${DATA_PATH}_lr${LR}_warm${WARMUP_RATIO}_gas${GRADIENT_ACCUMULATION_STEPS}_epoch${N_EPOCH} \
    --bf16 True \
    --plot_loss True \
    --ddp_timeout 180000000 \
    --include_num_input_tokens_seen True \
    --deepspeed ${ds_config}  \
    --save_only_model
