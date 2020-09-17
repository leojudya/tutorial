import asyncio
import websockets
import psutil
import time
import json
import os
    
async def hello(websocket, path):
    while True:
        j = {}        
        j["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        j["cpu"] = str(psutil.cpu_percent()) + "%"
        j["memory"] = str(psutil.virtual_memory().percent)
        # swap = str(psutil.swap_memory().percent)
        j["disk"] = []
        for part in psutil.disk_partitions(all=False):
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    continue
            usage = psutil.disk_usage(part.mountpoint)
            j["disk"].append({part.device:int(usage.percent)})
        await websocket.send(json.dumps(j, sort_keys=True, indent=4))
        await asyncio.sleep(1)
    

start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()