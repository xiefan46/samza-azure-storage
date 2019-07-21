#!/bin/bash


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


#install jupyter-notebook
sudo apt install jupyter-notebook

sudo pip3 install matplotlib

#increase open file limit
ulimit -S -n 50000
ulimit -H -n 50000
