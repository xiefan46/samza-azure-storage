from library.util import *
import os
import random
from library.IostatMonitorThread import *

'''
Use benchmark.sh instead of db_bench
'''

class Benchmark2():


    def __init__(self, test_dir, rocks_db_dir, para_map={"KEY_SIZE": 20, "VALUE_SIZE": 400}, verbose=True):
        self.rocks_db_dir = rocks_db_dir
        run_cmd(f"cp {rocks_db_dir}/db_bench .")
        os.system("cd {rocks_db_dir}")
        run_cmd(f"cp ../scripts/benchmark.sh {rocks_db_dir}/tools")
        self.benchmark_sh = f"{rocks_db_dir}/tools/benchmark.sh"
        self.para_map = para_map
        self.verbose = verbose
        self.test_dir = self.setup_test_env(test_dir)

    '''
    Bulkload:
        The keys are inserted in random order. 
        The database is empty at the beginning of this benchmark run and gradually fills up. 
        No data is being read when the data load is in progress.

        Rocksdb was configured to first load all the data in L0 with compactions switched off and using an unsorted vector    memtable. 
        Then it made a second pass over the data to merge-sort all the files in L0 into sorted files in L1. 
        Here are the commands we used for loading the data into rocksdb:
    '''

    def bulkload(self):
        print("running bulk load")
        self.run_benchmark_sh("bulkload")
        print("bulk load done")
        
    '''
    Random Write: Measure performance to randomly overwrite a large number of keys into the database. 
    The database was first created by the previous bulkload benchmark. 
    This benchmark was run with the Write-Ahead-Log (WAL) disabled and uses a single thread. 
    The Random Write benchmark can be used to measure the performance of accessing read-write state.
    Random Write is corresponding to the scenarios such as state required for joins of streams/tables 
    over a windows, aggregations, buffers, and machine learning models.

    '''
    def overwrite(self):
        print("running overwrite ")
        self.para_map["NUM_THREADS"] = 1
        self.run_benchmark_sh("overwrite")
        self.para_map.pop("NUM_THREADS", None)
        print("overwrite done")


    '''
    Random Read: Measure random read performance of a database. 
    Rocksdb was configured with a block size of 8KB. Data compression and Write-Ahead-Log (WAL) is disabled. 
    Random Read benchmark measures applications that look up “adjunct” read-only data.
    Many applications need to get the necessary information for each event to process it. 
    Samza apps that have this workload are SamzaSQL or Beam jobs that do key based joins, Filtering/Deduping jobs, etc.
    '''
    def readrandom(self):
        print("running readrandom ")
        self.para_map["NUM_THREADS"] = 1
        self.run_benchmark_sh("readrandom")
        self.para_map.pop("NUM_THREADS", None)
        print("readrandom done")


    def get_num_keys(self, data_size, key_size, value_size):
        return int(data_size / (key_size + value_size))

    def run_benchmark_sh(self, benchmarks):
        iostat_monitor_thread = IostatMonitorThread(f"iostat-{benchmarks}", self.iostat_dir)
        iostat_monitor_thread.start()
        cmd = f"{self.form_parameter_string(self.para_map)} {self.benchmark_sh} {benchmarks}"
        print(cmd)
        res = run_cmd(cmd)
        print(res)
        iostat_monitor_thread.stop()

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
        self.iostat_dir = f"{dir_name}/iostat_log"
        os.system("mkdir {}".format(self.db_dir))
        os.system("mkdir {}".format(self.wal_dir))
        os.system("mkdir {}".format(self.output_dir))
        os.system("mkdir {}".format(self.tmp_dir))
        os.system("mkdir {}".format(self.iostat_dir))
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