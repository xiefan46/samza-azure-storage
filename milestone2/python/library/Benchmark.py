from library.Constant import *
from library.util import *
import random
import os

@DeprecationWarning("Use Benchmark2 instead of this class")
class Benchmark():

    def __init__(self, root_dir, db_bench, key_size, value_size, data_size, other_params="",
                 save_res=True, verbose=True):
        self.db_bench = db_bench
        self.key_size = key_size
        self.value_size = value_size
        self.data_size = data_size
        self.other_params = other_params
        self.save_res = save_res
        self.verbose = verbose
        self.test_dir, self.performance_testing_log_dir = self.setup_test_env(root_dir)
        self.num_keys = self.get_num_keys(self.data_size, self.key_size, self.value_size)

    def fillseq(self):
        return self.run_db_bench(benchmarks="fillseq", use_existing_db=False)

    def readseq(self):
        return self.run_db_bench(benchmarks="readseq")

    def overwrite(self):
        return self.run_db_bench(benchmarks="overwrite")

    def readrandom(self):
        return self.run_db_bench(benchmarks="readrandom")

    def readwhilewriting(self):
        return self.run_db_bench(benchmarks="readwhilewriting")

    def deleterandom(self):
        return self.run_db_bench(benchmarks="deleterandom")

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
        res = self.run_db_bench(benchmarks="fillrandom", use_existing_db=False, other_params=parameter_bulkload)
        print("bulk load finish. Start to run compaction")
        # do compaction
        self.run_db_bench(benchmarks="compact", other_params="--disable_auto_compactions=1 \
                                                                --sync=0 \
                                                                --threads=1")
        return res

    '''
    Overwrite 1/100 of the KVs in the original DB with WAL disable
    '''

    def random_write(self):
        # num_keys = self.get_num_keys(self.data_size / 1000, self.key_size, self.value_size)
        num_keys = 10
        return self.run_db_bench(benchmarks="overwrite", num_keys=num_keys, other_params="--disable_wal=1")

    def benchmark_all(self):
        self.fillseq()
        self.readseq()
        self.overwrite()
        self.readrandom()
        self.readwhilewriting()

    def get_num_keys(self, data_size, key_size, value_size):
        return int(data_size / (key_size + value_size))

    def run_db_bench(self, benchmarks, use_existing_db=True, num_keys=-1, other_params=""):
        if num_keys <= 0:
            num_keys = self.get_num_keys(self.data_size, self.key_size, self.value_size)
        const_params = " --db={} --histogram=1 --num={} --use_existing_db={} --key_size={} --value_size={}  --block_size=4096 --compression_type=snappy --max_write_buffer_number=3 --cache_size=104857600 --write_buffer_size=33554432 --statistics {} ".format(
            self.test_dir, num_keys, 1 if use_existing_db else 0, self.key_size, self.value_size, other_params)

        command = "{} --benchmarks=\"{}\"  {} ".format(self.db_bench, benchmarks, const_params)
        if self.verbose:
            print("command : {}".format(command))
        res = run_cmd(command, False)
        if self.save_res == True:
            self.dump_res_to_file(command, res, benchmarks)
        if self.verbose == True:
            print(res)
        return res

    def dump_res_to_file(self, command, res, benchmarks):
        file_name = f"{self.performance_testing_log_dir}/{benchmarks}-{PERFORMANCE_RESULT_POSTFIX}"
        if self.verbose:
            print("Dump result to file : {}".format(file_name))
        file = open(file_name, "w+")
        file.write("{}\n\n".format(command))
        file.write(res)
        file.close()

    def setup_test_env(self, root_dir):
        test_dir = self.get_random_test_dir(root_dir)
        performance_testing_log_dir = f"{test_dir}/{PERFORMANCE_RES_DIR_NAME}"
        # if self.verbose:
        print("Setup a new test root. Test root dir {}".format(test_dir))
        self.create_new_dir(test_dir)
        self.create_new_dir(performance_testing_log_dir)
        return test_dir, performance_testing_log_dir

    def create_new_dir(self, dir_name):
        os.system("rm -rf {}".format(dir_name))
        os.system("mkdir {}".format(dir_name))

    def get_random_test_dir(self, root_dir):
        return "{}/test-{}".format(root_dir, random.randint(0, 1000000000))
