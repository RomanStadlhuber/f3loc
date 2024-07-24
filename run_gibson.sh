#!/bin/bash
### use this script to evaluate the method on gibson dataset
source .env
python3 eval_filtering.py \
    --net_type d \
    --traj_len 100 \
    --dataset_path /mnt/amcl/f3loc/Gibson \
    --ckpt_path /mnt/amcl/f3loc/weights \
    --evol_path /mnt/amcl/f3loc/results