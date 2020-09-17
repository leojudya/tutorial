import psutil
import time
import json
import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    j = {}        
    j["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    j["cpu"] = str(psutil.cpu_percent()) + "%"
    j["memory"] = str(psutil.virtual_memory().percent)
    j["disk"] = []
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                continue
        usage = psutil.disk_usage(part.mountpoint)
        j["disk"].append({part.device:int(usage.percent)})
    return json.dumps(j, sort_keys=True, indent=4)
    
