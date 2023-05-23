#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
HOST_DIR=$(echo $SCRIPT_DIR | sed 's/\/workspace/~/')

function cleanup {
  echo "$HOST_DIR/fans_auto.sh" > $SCRIPT_DIR/pipe
  exit
}
trap cleanup EXIT

# Turn fans to max when running experiment
# bash $SCRIPT_DIR/fans_max.sh
echo "$HOST_DIR/fans_max.sh" > $SCRIPT_DIR/pipe

python $SCRIPT_DIR/run.py with \
  data_root=data/arrow \
  num_gpus=2 \
  num_nodes=1 \
  task_finetune_itm_with_embedding \
  whole_word_masking=True \
  step200k \
  per_gpu_batchsize=8 \
  load_path=$SCRIPT_DIR/checkpoints/provided_vlmo/vlmo_base_patch16_224.pt \
  log_dir=logs