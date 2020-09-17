import asyncio
import websockets
import time
import psutil
import os
from psutil._common import bytes2human

    
async def hello(websocket, path):
    while True:
        cpu_percent = "CPU: " + str(psutil.cpu_percent()) + "%"
        await websocket.send(cpu_percent)
        vir = str(psutil.virtual_memory().percent)
        swap = str(psutil.swap_memory().percent)
        await websocket.send(vir)
        await websocket.send(swap)
        await websocket.send("End")
        for part in psutil.disk_partitions(all=False):
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    # skip cd-rom drives with no disk in it; they may raise
                    # ENOENT, pop-up a Windows GUI error for a non-ready
                    # partition or just hang.
                    continue
            usage = psutil.disk_usage(part.mountpoint)
            await websocket.send(f"{part.device} {int(usage.percent)}")
        temps = psutil.sensors_temperatures()
        for name, entries in temps.items():
            await websocket.send("    %-20s %s °C (high = %s °C, critical = %s °C)" % (
                entry.label or name, entry.current, entry.high,
                entry.critical))
        await asyncio.sleep(1)

    

start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()