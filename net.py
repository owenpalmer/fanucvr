# import asyncio
# import websockets
# import json
# # Example of sending a dictionary as JSON
# # await websocket.send(json.dumps({"time": "12:00", "message": "Hello from server!"}))

# async def echo(websocket, path):
#     async for message in websocket:
#         await websocket.send(f"Server received: {message}")

# # start_server = websockets.serve(echo, "localhost", 8765)
# start_server = websockets.serve(echo, "192.168.137.1", 8765)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()
import asyncio
import websockets
from datetime import datetime  # Import the datetime class from the datetime module

async def time(websocket, path):
    async for message in websocket:
        await websocket.send(f"Server received: {message}")
    while True:
        await asyncio.sleep(1)  # Wait for 1 second
        message = "Current server time is: {}".format(datetime.now().strftime("%H:%M:%S"))
        await websocket.send(message)  # Send message to the client

start_server = websockets.serve(time, "192.168.137.1", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
