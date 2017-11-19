import numpy as np
import pyautogui
import cv2
from PIL import Image

def find_mob(radar):
    mob = (250, 60, 50)
    mobs = []
    for y in range(147):
        b = []
        for x in range(147):
            if radar.getpixel((x, y)) == mob:
                b.append((x, y))

            else: b.append(None)

        mobs.append(b)

    return mobs
            
    

#while True:
screen = pyautogui.screenshot('ss.png', region=(0, 80, 1024, 716))
radar = screen.crop((876, 537, 1023, 684))
radar.save('radar.png')
mobs = find_mob(radar)


