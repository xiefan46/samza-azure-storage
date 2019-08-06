#!/bin/bash

#example: bash ~/milestone2/scripts/mount_disks.sh /dev/sdf /dev/sdf1 /read_cache2
root_dir=$1
target_dir=$2

cp -r $root_dir/output $target_dir
cp -r $root_dir/iostat_log $target_dir
cp $root_dir/db/LOG* $target_dir/output
