import numpy as np
import pyautogui
import cv2, math, time, directkeys

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
        return math.asin(mob_x/mob_h) * 180/math.pi
    except:
        return 0

def track():
    z = 0x2C
    c = 0x2E
    key = None
    
    while True:
        screen = pyautogui.screenshot(region=(0, 80, 1024, 716))
        radar = screen.crop((876, 537, 1023, 684))
    
        mobs = find_mob(radar)
        deg = mob_to_parallel(closest_mob(mobs))
        print(deg)
        
        
        if deg > 10:
            if key != None:
                directkeys.ReleaseKey(key)
            key = c
            directkeys.PressKey(c)
        elif deg < -10:
            if key != None:
                directkeys.ReleaseKey(key)
            key = z
            directkeys.PressKey(z)

        else:
            if key == None:
                break
            
            directkeys.ReleaseKey(key)
            break

        time.sleep(.05)
                
while True:
    track()

