import numpy as np
import pyautogui
import cv2

from scipy import ndimage
from scipy import misc

from PIL import Image

def find_mob(radar):
    mob = (250, 60, 50)
    mobs = []
    for y in range(147):
        b = []
        for x in range(147):
            if radar.getpixel((x, y)) == mob:
                b.append(1)

            else: b.append(0)

        mobs.append(b)

    structure = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    mobs, mob_count = ndimage.measurements.label(mobs, structure=structure)

    b = {}
    for i in range(mob_count):
        b[i] = list()

    class BreakIt(Exception): pass
    
    for y in range(len(mobs)):
        for x in range(len(mobs)):
            if mobs[y][x] != 0:
                b[mobs[y][x] - 1].append((x, y))

    mobs = []
    for k in b.keys():
        i = int(len(b[k])/2)
        mobs.append(b[k][i])

    return mobs

#while True:
screen = pyautogui.screenshot('ss.png', region=(0, 80, 1024, 716))
radar = screen.crop((876, 537, 1023, 684))
radar.save('radar.png')
mobs = find_mob(radar)
print(mobs)

