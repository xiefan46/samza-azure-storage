import threading
from library.util import *
import datetime


'''
You can use this class to start an IOStat daemon when every benchmark starts. 
Remember to stop this thread when your benchmark ends. 
'''
class IostatMonitorThread(threading.Thread):
    def __init__(self, name, output_dir): 
        threading.Thread.__init__(self) 
        self.name = name 
        self.output_file_name = f"{output_dir}/iostat-{self.name}.log"
              
    def run(self): 
  
        # target function of the thread class 
        try: 
            self.kill_all_iostat()
            print(f"iostat monitor thread : {self.name} start. timestamp : {datetime.datetime.now()}")
            cmd = "iostat 1 | awk '{now=strftime(\"%Y-%m-%d %T \"); print now $0}'  > " + self.output_file_name
            run_cmd(cmd)
        except AssertionError:
            pass
        finally: 
            print(f"iostat monitor thread : {self.name} end. timestamp : {datetime.datetime.now()}")  
    
    def stop(self):
        self.kill_all_iostat()
    
    def kill_all_iostat(self):
        ids = run_cmd("pgrep iostat").split("\n")
        for pid in ids:
            run_cmd(f"kill {pid}")
        
