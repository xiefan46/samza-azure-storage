#!/bin/bash


echo $project_dir

#install RocksDB
cd ~/

git clone https://github.com/facebook/rocksdb.git

cd rocksdb

git checkout -b rocksdb6.1.2 tags/v6.1.2

sudo apt install g++

#install libraries for RocksDB
sudo apt-get install libsnappy-dev

sudo apt-get install libgflags-dev

sudo apt install make

#compile RocksDB
make release

#overwrite the benchmark.sh script because we want to disable WAL
cp ~/samza-azure-storage/milestone2/scripts/benchmark.sh ~/rocksdb/tools

#install jupyter-notebook
sudo apt install jupyter-notebook

sudo pip3 install matplotlib

#increase open file limit
ulimit -S -n 50000
ulimit -H -n 50000

#install fio to test random read/write of disk
sudo apt install fio

#install iostat
sudo apt-get install sysstat -y