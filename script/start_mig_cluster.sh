#!/bin/bash
uuids=$(nvidia-smi -L | grep "MIG" | grep -oP '(?<=UUID: ).*(?=\))')
uuids=$(echo $uuids | sed 's/ /,/g')
device_num=$(nvidia-smi -L | grep "MIG" | wc -l)

CUDA_VISIBLE_DEVICES=$uuids ray start --head --num-gpus ${device_num}
