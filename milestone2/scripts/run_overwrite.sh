#!/bin/bash

#Run overwrite manually. This script is used for test cloning and re-mounting latency  
banchmark_sh=$1
root_dir=$2

source "KEY_SIZE=20 VALUE_SIZE=400 DB_DIR=$root_dir/db OUTPUT_DIR=$root_dir/output WAL_DIR=$root_dir/wal TEMP=$root_dir/tmp COMPRESSION_TYPE=none CACHE_SIZE=104857600 NUM_KEYS=25000000 NUM_THREADS=1 $benchmark_sh overwrite"


