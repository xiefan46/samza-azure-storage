from util import *
import datetime
import json
import random
from Constant import *
import os



class IOBenchmark():

    def __init__(self, block_size, data_size, output_dir, clean_up=True):
        self.block_size = block_size
        self.data_size = data_size
        self.output_dir, self.performance_testing_log_dir = self.setup_test_env(output_dir)
        self.clean_up = clean_up
        self.count = self.get_block_count(self.data_size, self.block_size)

    def fio_sequential_read(self, file_name):
        print(f"running sequential_read. timestamp : {datetime.datetime.now()}")
        cmd = f"fio -filename={file_name}   -rw=read  -bs={self.block_size} -size={self.data_size} -numjobs=1 -name=mytest\
         --output-format=json"
        print(cmd)
        res = run_cmd(cmd, True)
        return res

    def fio_sequential_write(self, file_name):
        print(f"running sequential_write. timestamp : {datetime.datetime.now()}")
        cmd = f"fio -filename={file_name} -rw=write -bs={self.block_size} -size={self.data_size} -numjobs=1 -name=mytest\
         --output-format=json"
        print(cmd)
        res = run_cmd(cmd, True)
        return res

    def fio_sequential_readwrite(self):
        print(f"sequential benchmark using fio")
        output_file_name = self.get_output_file_name("fio", self.output_dir)
        self.delete_file(output_file_name)
        write_res = self.fio_sequential_write(output_file_name)
        read_res = self.fio_sequential_read(output_file_name)
        if self.clean_up == True:
            self.delete_file(output_file_name)
        return read_res, write_res

    def fio_random_read(self, file_name):
        print(f"running random_read. timestamp : {datetime.datetime.now()}")
        cmd = f"fio -filename={file_name} -rw=randread -bs={self.block_size} -size={self.data_size / 10} -numjobs=1 -name=mytest\
         --output-format=json "
        print(cmd)
        res = run_cmd(cmd, True)
        return res

    def fio_random_write(self, file_name):
        print(f"running random_write. timestamp : {datetime.datetime.now()}")
        cmd = f"fio -filename={file_name} -rw=randwrite -bs={self.block_size} -size={self.data_size} \
        -numjobs=1 -name=mytest --output-format=json"
        print(cmd)
        res = run_cmd(cmd, True)
        return res

    def fio_random_readwrite(self):
        print("random benchmark using fio")
        output_file_name = self.get_output_file_name("fio", self.output_dir)
        self.delete_file(output_file_name)
        write_res = self.fio_random_write(output_file_name)
        read_res = self.fio_random_read(output_file_name)
        if self.clean_up == True:
            self.delete_file(output_file_name)
        return read_res, write_res

    # example : dic["jobs"][0]["write"]["bw_mean"]
    def extract_throughput_mb(self, json_str, rw_type):
        dic = json.loads(json_str)
        res = float(dic["jobs"][0][rw_type]["bw"])
        return int(res / 1024)

    def delete_file(self, file_name):
        os.system(f"rm -rf {file_name}")

    def get_block_count(self, data_size, block_size):
        return int(data_size / block_size)

    def get_output_file_name(self, tool_name, output_dir):
        file_name = f"{output_dir}/test-{tool_name}-{random.randint(0, 1000000000)}"
        return file_name

    def run_all_and_extract_throughput(self):
        fio_seq_read_res, fio_seq_write_res = self.fio_sequential_readwrite()
        fio_random_read_res, fio_random_write_res = self.fio_random_readwrite()
        seq_read_res = self.extract_throughput_mb(fio_seq_read_res, "read")
        seq_write_res = self.extract_throughput_mb(fio_seq_write_res, "write")
        random_read_res = self.extract_throughput_mb(fio_random_read_res, "read")
        random_write_res = self.extract_throughput_mb(fio_random_write_res, "write")
        print(f"seq read : {seq_read_res} MB/s. seq write : {seq_write_res} MB/s. \
          random read : {random_read_res} MB/s. random write : {random_write_res} MB/s")

    def run_all_and_dump_files(self):
        fio_seq_read_res, fio_seq_write_res = self.fio_sequential_readwrite()
        fio_random_read_res, fio_random_write_res = self.fio_random_readwrite()
        self.dump_res_to_file(fio_seq_read_res, "fio_seq_read_res")
        self.dump_res_to_file(fio_seq_write_res, "fio_seq_write_res")
        self.dump_res_to_file(fio_random_read_res, "fio_random_read_res")
        self.dump_res_to_file(fio_random_write_res, "fio_random_write_res")

    def run_seq_and_extract_throughput(self):
        fio_seq_read_res, fio_seq_write_res = self.fio_sequential_readwrite()
        seq_read_res = self.extract_throughput_mb(fio_seq_read_res, "read")
        seq_write_res = self.extract_throughput_mb(fio_seq_write_res, "write")
        # self.dump_res_to_file(seq_read_res, "seq_read_res")
        # self.dump_res_to_file(seq_write_res, "seq_write_res")
        print(f"seq read : {seq_read_res} MB/s. seq write : {seq_write_res} MB/s.")

    def run_random_and_extract_throughput(self):

        fio_random_read_res, fio_random_write_res = self.fio_random_readwrite()

        random_read_res = self.extract_throughput_mb(fio_random_read_res, "read")
        random_write_res = self.extract_throughput_mb(fio_random_write_res, "write")
        # self.dump_res_to_file(random_read_res, "random_read_res")
        # self.dump_res_to_file(random_write_res, "random_write_res")
        print(f"random read : {random_read_res} MB/s. random write : {random_write_res} MB/s")

    def dump_res_to_file(self, res, benchmarks):
        file_name = f"{self.performance_testing_log_dir}/{benchmarks}-{PERFORMANCE_RESULT_POSTFIX}"
        file = open(file_name, "w+")
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