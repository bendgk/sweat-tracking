import numpy as np
import pyautogui
import cv2, math, time

from scipy import ndimage
from scipy import misc

from PIL import Image

pyautogui.FAILSAFE = True
center = (73, 75)

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

def closest_mob(mobs):
    try:
        d = []
        for i in mobs:
            d.append(math.sqrt((i[0] - center[0])**2 + (i[1] - center[1])**2))
        return mobs[d.index(min(d))]
    except:
        print("No mobs in vicinity!")

def mob_to_parallel(mob):
    try:
        mob_h = math.sqrt((mob[0] - center[0])**2 + (mob[1] - center[1])**2)
        mob_x = mob[0] - center[0]
        mob_y = mob[1] - center[1]

        #if mob_y < 0: mob_h = -mob_h
        
        print(mob_x, mob_y, mob_h)
        return math.asin(mob_x/mob_h)
    except:
        return 0

def track(mob):
    while True:
        deg = mob_to_parallel(mob)
        if deg < 0:
            pyautogui.keyDown('c')
            time.sleep(.1)
            pyautogui.keyUp('c')
        else:
            pyautogui.keyDown('z')
            time.sleep(.1)
            pyautogui.keyUp('z')

#while True:
screen = pyautogui.screenshot('ss.png', region=(0, 80, 1024, 716))
radar = screen.crop((876, 537, 1023, 684))
radar.save('radar.png')
mobs = find_mob(radar)
print(mobs)
print(mob_to_parallel(closest_mob(mobs))*180/math.pi)

track(closest_mob(mobs))
