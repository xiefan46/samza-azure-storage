#!/bin/bash

#add your public ssh key of this vm to github first

git clone https://github.com/xiefan46/samza-azure-storage.git

cd ~/samza-azure-storage/milestone2

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



