#!/bin/bash

disk_location=$1
disk_name=$2
mount_dir_name=$3

(echo n; echo p; echo 1; echo ; echo ; echo w) | sudo fdisk $disk_location
sudo mkfs -t ext4 $disk_name
sudo mkdir $mount_dir_name && sudo mount $disk_name $mount_dir_name
sudo chmod 777 $mount_dir_name