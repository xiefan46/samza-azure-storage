import os
import random
import util

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

    def benchmark_all(self):
        self.fillseq()
        self.readseq()
        self.overwrite()
        self.readrandom()
        self.readwhilewriting()

    def get_num_keys(self, data_size, key_size, value_size):
        return int(data_size / (key_size + value_size))

    def run_db_bench(self, benchmarks, use_existing_db=True):

        num_keys = self.get_num_keys(self.data_size, self.key_size, self.value_size)
        const_params = "\
          --db={} \
          --histogram=1 \
          --num={} \
          --use_existing_db={} \
          --key_size={} \
          --value_size={}  \
          --statistics {}".format(self.test_dir, num_keys, 1 if use_existing_db else 0, self.key_size, self.value_size,
                                  self.other_params)
        command = "{} --benchmarks=\"{}\"  {} ".format(self.db_bench, benchmarks, const_params)
        if self.verbose:
            print("command : {}".format(command))
        res = util.run_cmd(command, False)
        if self.save_res == True:
            self.dump_res_to_file(command, res, benchmarks)
        if self.verbose == True:
            print(res)
        return res

    def dump_res_to_file(self, command, res, benchmarks):
        file_name = "{}/{}-performance-result".format(self.performance_testing_log_dir, benchmarks)
        if self.verbose:
            print("Dump result to file : {}".format(file_name))
        file = open(file_name, "w+")
        file.write("{}\n\n".format(command))
        file.write(res)
        file.close()

    def setup_test_env(self, root_dir):
        test_dir = self.get_random_test_dir(root_dir)
        performance_testing_log_dir = "{}/performance-testing-log".format(test_dir)
        if self.verbose:
            print("Setup a new test root. Test root dir {}".format(test_dir))
        self.create_new_dir(test_dir)
        self.create_new_dir(performance_testing_log_dir)
        return test_dir, performance_testing_log_dir

    def create_new_dir(self, dir_name):
        os.system("rm -rf {}".format(dir_name))
        os.system("mkdir {}".format(dir_name))

    def get_random_test_dir(self, root_dir):
        return "{}/test-{}".format(root_dir, random.randint(0, 1000000000))

