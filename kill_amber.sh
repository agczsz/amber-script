#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <GPU_ID>"
    exit 1
fi

GPU_ID=$1

for i in {1..20}; do
    pid=$(nvidia-smi | grep amber | awk -v gpu="$GPU_ID" '$2==gpu {print $5}')
    
    if [[ -n "$pid" ]]; then
        kill -9 $pid
        echo "Attempt $i: amber process ($pid) on GPU=$GPU_ID killed"
    else
        echo "Attempt $i: No amber process found on GPU=$GPU_ID"
    fi
    
    sleep 1
done
