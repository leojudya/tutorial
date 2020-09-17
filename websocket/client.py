import asyncio
import websockets
import time

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            cpu = await websocket.recv()
            print(f"{cpu}")
            time.sleep(1)

asyncio.get_event_loop().run_until_complete(hello())