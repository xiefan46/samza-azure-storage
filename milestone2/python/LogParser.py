
class LogParser():
    def __init__(self, log):
        self.log = log
        self.lines = log.split("\n")

    def parse_all(self):
        self.base_res_line = None
        self.delay_percentiles_line = None
        for line in self.lines:
            self.extract_basic_res_line(line)
            self.extract_delay_percentiles_line(line)

    def extract_basic_res_line(self, line):
        if self.base_res_line == None and "micros/op" in line and "ops/sec" in line and "MB/s" in line:
            self.base_res_line = line

    def extract_delay_percentiles_line(self, line):
        if self.delay_percentiles_line == None and line.startswith("Percentiles: P50"):
            self.delay_percentiles_line = line

    def dump(self):
        print(self.base_res_line)
        print(self.delay_percentiles_line)

    def get_basic_res(self):
        return self.convert_to_dict(["micros/op", "ops/sec", "MB/s"], self.extract_float(self.base_res_line))

    def get_percentiles(self):
        return self.convert_to_dict(["P50", "P75", "P99", "P99.9", "P99.99"],
                                    self.extract_float(self.delay_percentiles_line))

    def extract_float(self, line):
        strs = self.delay_percentiles_line.split(" ")
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