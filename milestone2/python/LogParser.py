from Constant import *

class LogParser():
    def __init__(self, log=None, file_name=None):
        if file_name != None:
            log = open(file_name, 'r').read()
        self.log = log
        self.lines = log.split("\n")

    def parse_all(self, res=None):
        self.base_res_line = None
        self.delay_percentiles_line = None
        for line in self.lines:
            self.extract_basic_res_line(line)
            self.extract_delay_percentiles_line(line)
        if res != None:
            res.put_all_res(self.get_basic_res())
            res.put_all_res(self.get_percentiles())

    def extract_basic_res_line(self, line):
        if self.base_res_line == None and "micros/op" in line and "ops/sec" in line:
            self.base_res_line = line

    def extract_delay_percentiles_line(self, line):
        if self.delay_percentiles_line == None and line.startswith("Percentiles: P50"):
            self.delay_percentiles_line = line

    def dump(self):
        print(self.base_res_line)
        print(self.delay_percentiles_line)

    def get_basic_res(self):
        d = self.extract_float(self.base_res_line)
        # print(self.base_res_line)
        # print(d)
        return self.convert_to_dict([LOG_RES_MICORS_OP, LOG_RES_OPS_SEC, LOG_RES_THROUGHPUT], d)

    def get_percentiles(self):
        return self.convert_to_dict([LOG_RES_P50, LOG_RES_P75, LOG_RES_P99, LOG_RES_P999, LOG_RES_P9999],
                                    self.extract_float(self.delay_percentiles_line))

    def extract_float(self, line):
        strs = line.split(" ")
        res_list = []
        for s in strs:
            if self.is_float(s):
                res_list.append(float(s))
        return res_list

    def convert_to_dict(self, name_list, num_list):
        res_dict = {}
        for i in range(len(name_list)):
            res_dict[name_list[i]] = num_list[i]
        return res_dict

    def is_float(self, s):
        try:
            f = float(s)
            return True
        except:
            return False