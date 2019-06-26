import matplotlib.pyplot as plt; plt.rcdefaults()
from subprocess import Popen, PIPE


#command line tool
def run_cmd(cmd, throw_exception = False):
    p = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    out_str = out.decode("utf-8")
    err_str = err.decode("utf-8")
    if(throw_exception and err_str != ''):
        raise Exception(err_str)
    return out_str


