import asyncio
import websockets
import time
import psutil
import os
from psutil._common import bytes2human

    
async def hello(websocket, path):
    while True:
        t = time.strftime("%Y-%M-%d %H:%M:%S", time.localtime())
        await websocket.send(t)
        cpu_percent = "CPU: " + str(psutil.cpu_percent()) + "%"
        await websocket.send(cpu_percent)
        vir = str(psutil.virtual_memory().percent)
        swap = str(psutil.swap_memory().percent)
        await websocket.send(vir)
        await websocket.send(swap)
        for part in psutil.disk_partitions(all=False):
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    # skip cd-rom drives with no disk in it; they may raise
                    # ENOENT, pop-up a Windows GUI error for a non-ready
                    # partition or just hang.
                    continue
            usage = psutil.disk_usage(part.mountpoint)
            await websocket.send(f"{part.device} {int(usage.percent)}")
        await websocket.send("End")

        await asyncio.sleep(1)

    

start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()