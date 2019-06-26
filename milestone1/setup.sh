#!/bin/bash

(echo n; echo p; echo 1; echo ; echo ; echo w) | sudo fdisk /dev/sdc
sudo mkfs -t ext4 /dev/sdc1
sudo mkdir /datadrive && sudo mount /dev/sdc1 /datadrive
sudo chmod 777 /datadrive