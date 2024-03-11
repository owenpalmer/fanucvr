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
from io import BytesIO

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

# img = ImageGrab.grab(bbox=(left+150, top+240, right-150, bottom-1000))

def get_difference(image1, image2):
    if image1.size != image2.size:
        print("Images are not the same size")
    else:
        # Convert images to RGB if they are not
        if image1.mode != 'RGB':
            image1 = image1.convert('RGB')
        if image2.mode != 'RGB':
            image2 = image2.convert('RGB')

        # Get the pixel data
        pixels1 = image1.load()
        pixels2 = image2.load()

        # Store differences
        differences = []

        # Compare the pixel data
        for y in range(image1.size[1]):  # Iterate over rows
            for x in range(image1.size[0]):  # Iterate over columns
                if pixels1[x, y] != pixels2[x, y]:
                    differences.append(((x, y), pixels1[x, y]))
    return differences

# Capture the window area using PIL's ImageGrab
# while True:
#     img = ImageGrab.grab(bbox=(left, top, right, bottom))
#     diff = get_difference(img, prev)
#     prev = img

# Save the image
# img.save("captured_window.png")
# print("Image saved as 'captured_window.png'.")

def img_grab(win):
    right, left, top, bottom = win.right, win.left, win.top, win.bottom
    img = ImageGrab.grab(bbox=(left+150, top+240, right-150, bottom-1000))
    return img


def get_image_str(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

print(win.size)

async def echo(websocket, path):
    # async for message in websocket:
    #     if message=="size":
    #         await websocket.send(json.dumps({"size": win.size}))
    # img = ImageGrab.grab(bbox=(left, top, right, bottom))
    img = img_grab(win)
    prev = img_grab(win)
    while True:
        img = img_grab(win)
        f = 0.5
        size = (int(img.width*f),int(img.height*f))
        diff = get_difference(img.resize(size, Image.BICUBIC), prev.resize(size, Image.BICUBIC))
        # diff = get_difference(img, prev)
        if diff:
            # print("hi")
            await websocket.send(json.dumps({"diff": diff}))
        prev = img

start_server = websockets.serve(echo, "192.168.137.1", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()