import numpy as np
import pyautogui
import cv2, math, time, directkeys

from scipy import ndimage
from scipy import misc

from PIL import Image

pyautogui.FAILSAFE = True
center = (73, 75)

#Keys
z = 0x2C
c = 0x2E
w = 0x11
target = 0x0B
operate = 0x12
auto_operate = 0x02
loot = 0x0A
deselect = 0x0C

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
        return None

def mob_to_parallel(mob):
    try:
        mob_h = math.sqrt((mob[0] - center[0])**2 + (mob[1] - center[1])**2)
        mob_x = mob[0] - center[0]
        mob_y = mob[1] - center[1]

        #if mob_y < 0: mob_h = -mob_h
        return [math.asin(mob_x/mob_h) * 180/math.pi, mob_h]
    except:
        return [0, 0]

def in_range(distance_threshold):
    screen = pyautogui.screenshot(region=(0, 80, 1024, 716))
    radar = screen.crop((876, 537, 1023, 684))
    mobs = find_mob(radar)
    if closest_mob(mobs) == None:
        return False
    deg, distance = mob_to_parallel(closest_mob(mobs))

    return distance < distance_threshold

def track(distance_threshold, degree_threshold):
    key = None

    screen = pyautogui.screenshot(region=(0, 80, 1024, 716))
    radar = screen.crop((876, 537, 1023, 684))
    mobs = find_mob(radar)
    if closest_mob(mobs) == None:
        return False
    deg, distance = mob_to_parallel(closest_mob(mobs))
    #print(deg, distance)

    while distance > distance_threshold or abs(deg) > degree_threshold:
        print("searching")
        screen = pyautogui.screenshot(region=(0, 80, 1024, 716))
        radar = screen.crop((876, 537, 1023, 684))

        mobs = find_mob(radar)
        deg, distance = mob_to_parallel(closest_mob(mobs))

        #print(deg, distance)

        if deg > degree_threshold:
            if key != None:
                directkeys.ReleaseKey(key)
            key = c
            directkeys.PressKey(c)
        elif deg < -degree_threshold:
            if key != None:
                directkeys.ReleaseKey(key)
            key = z
            directkeys.PressKey(z)
        else:
            if key == None:
                pass

            else: directkeys.ReleaseKey(key)

        directkeys.PressKey(w)
        #time.sleep(.05)

    if key != None: directkeys.ReleaseKey(key)
    directkeys.ReleaseKey(w)

    return distance < distance_threshold and abs(deg) < degree_threshold

def template_match(template, write_out = False):
    img_rgb = np.array(pyautogui.screenshot(region=(0, 80, 1024, 716)))
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template,0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    matched = False

    for pt in zip(*loc[::-1]):
        matched = True
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

    if write_out:
        cv2.imwrite('res.png',img_rgb)

    return matched

def workout():
    directkeys.PressKey(target)
    time.sleep(.05)
    directkeys.ReleaseKey(target)
    directkeys.PressKey(auto_operate)
    time.sleep(.05)
    directkeys.ReleaseKey(auto_operate)

if __name__ == '__main__':
    working = False
    while True:
        #screenshot = pyautogui.screenshot('game.png', region=(0, 80, 1024, 716))
        while template_match('dead.jpg'):
            working = False
            directkeys.PressKey(loot)
            time.sleep(.05)
            directkeys.ReleaseKey(loot)
        if not in_range(8):
            track(6, 10)
        elif not working:
            workout()
            working = True
