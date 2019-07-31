from util import *
import os
import random
'''
Use benchmark.sh instead of db_bench
'''

class Benchmark2():

    # export DB_DIR=/raid/db
    # export WAL_DIR=/raid/wal
    # export TEMP=/raid/tmp
    # export OUTPUT_DIR=/raid/output

    def __init__(self, test_dir, rocks_db_dir, para_map={"KEY_SIZE": 20, "VALUE_SIZE": 400}, verbose=True):
        self.rocks_db_dir = rocks_db_dir
        run_cmd(f"cp {rocks_db_dir}/db_bench .")
        os.system("cd {rocks_db_dir}")
        self.benchmark_sh = f"{rocks_db_dir}/tools/benchmark.sh"
        self.para_map = para_map
        self.verbose = verbose
        self.test_dir = self.setup_test_env(test_dir)

    '''
    Bulkload:
        The keys are inserted in random order. 
        The database is empty at the beginning of this benchmark run and gradually fills up. 
        No data is being read when the data load is in progress.

        Rocksdb was configured to first load all the data in L0 with compactions switched off and using an unsorted vector memtable. 
        Then it made a second pass over the data to merge-sort all the files in L0 into sorted files in L1. 
        Here are the commands we used for loading the data into rocksdb:
    '''

    def bulkload(self):
        print("running bulk load")
        self.run_benchmark_sh("bulkload")
        print("bulk load done")

    def overwrite(self):
        print("running overwrite load")
        self.run_benchmark_sh("overwrite")
        print("overwrite done")

    def get_num_keys(self, data_size, key_size, value_size):
        return int(data_size / (key_size + value_size))

    def run_benchmark_sh(self, benchmarks):
        os.system(f"{self.form_parameter_string(self.para_map)} {self.benchmark_sh} {benchmarks}")

    def setup_test_env(self, root_dir):
        test_dir = self.get_random_test_dir(root_dir)

        print("Setup a new test root. Test root dir {}".format(test_dir))
        self.create_new_dir(test_dir)

        return test_dir

    def create_new_dir(self, dir_name):
        os.system("rm -rf {}".format(dir_name))
        os.system("mkdir {}".format(dir_name))
        self.db_dir = f"{dir_name}/db"
        self.wal_dir = f"{dir_name}/wal"
        self.output_dir = f"{dir_name}/output"
        self.tmp_dir = f"{dir_name}/tmp"
        os.system("mkdir {}".format(self.db_dir))
        os.system("mkdir {}".format(self.wal_dir))
        os.system("mkdir {}".format(self.output_dir))
        os.system("mkdir {}".format(self.tmp_dir))
        self.para_map["DB_DIR"] = self.db_dir
        self.para_map["OUTPUT_DIR"] = self.output_dir
        self.para_map["WAL_DIR"] = self.wal_dir
        self.para_map["TEMP"] = self.tmp_dir

    def clean_up(self):
        os.system("rm -rf db_bench")

    def get_random_test_dir(self, root_dir):
        return "{}/test-{}".format(root_dir, random.randint(0, 1000000000))

    def form_parameter_string(self, kvs):
        res = ""
        for key, value in kvs.items():
            res = f"{res} {key}={value}"
        return res