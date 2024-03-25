# from PIL import Image, ImageChops, ImageResampling, ImageGrab
from PIL import Image, ImageChops, ImageGrab
import pygetwindow as gw
import os
import ctypes
import threading
import asyncio
import websockets
import json
import base64
import time
import io
import base64

# Makes the process DPI aware. If this is not set, the ImageGrab is off by the scale factor in windows display settings
ctypes.windll.user32.SetProcessDPIAware()

# title_contains = "Wabbitemu"
title_contains = "Wabbitemu"
windows = gw.getAllWindows()
for index, window in enumerate(windows):
    if title_contains in window.title:
        win = windows[index]
        break

win.activate()

# Ensure the window is not minimized (optional, based on need)
if win.isMinimized:
    win.restore()

# Get the dimensions of the window
right, left, top, bottom = win.right, win.left, win.top, win.bottom

def activate_window_periodically(win, interval):
    while True:
        time.sleep(interval)
        try:
            if not win.isActive:
                win.activate()
            if win.isMinimized:
                win.restore()
        except Exception as e:
            print(f"Error: {e}")

# thread = threading.Thread(target=activate_window_periodically, args=(win, 0.5))  # 0.5 seconds interval
# thread.daemon = True  # Allows the thread to be killed when the main program exits
# thread.start()

def img_grab(win):
    right, left, top, bottom = win.right, win.left, win.top, win.bottom
    img = ImageGrab.grab(bbox=(left+150, top+240, right-150, bottom-1000))
    return img

def get_image_str(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

print(win.size)

async def echo(websocket, path):
    # async for message in websocket:
    #     if message=="size":
    #         await websocket.send(json.dumps({"size": win.size}))
    while True:
        image = img_grab(win)
        img_str = get_image_str(image)
        print("hi")
        await websocket.send(json.dumps({"image": img_str}))

start_server = websockets.serve(echo, "localhost", 8765)
# start_server = websockets.serve(echo, "192.168.137.1", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()