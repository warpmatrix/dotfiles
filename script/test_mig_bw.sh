#!/bin/bash

ALL_MIG_GPUS=$(nvidia-smi -L | grep "UUID: MIG" | cut -d' ' -f 13 | cut -d')' -f 1)

for gpu in $(echo "$ALL_MIG_GPUS"); do
    CUDA_VISIBLE_DEVICES=$gpu ./a.out &
done

wait
