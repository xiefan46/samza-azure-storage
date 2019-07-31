class Result():
    def __init__(self, res_map={}):
        self.res_map = res_map

    def put_res(self, key, value):
        self.res_map[key] = value

    def put_all_res(self, res_map):
        self.res_map.update(res_map)