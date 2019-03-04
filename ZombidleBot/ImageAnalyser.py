import cv2
import numpy as np
import pytesseract
from .settings.Rectangle import Rectangle
from .settings.Point import Point

def findTemplateInImage(img, template):
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF)
    w, h = template.shape[::-1]
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return Rectangle.fromValues(max_loc[0], max_loc[1], max_loc[0] + w, max_loc[1] + h)

def readCharacters(img, box):
    return pytesseract.image_to_string(img[box.getSliceNP()]).replace("\n", "").replace("\r", "")

def findCenterSameColorHor(img, box, nb_pixel_min, color_min, color_max):
    crop = img[box.getSliceNP()]
    #todo : check that heigth = 1 else warn or something
    l = []
    p = False
    e = -1
    q = -1
    c = 0
    crop = np.append(crop, [0])
    #print(crop)
    for i in range(len(crop)):
        if crop[i] >= color_min and crop[i] <= color_max:
            if p == False:
                e = i
                p = True
            else:
                c += 1
        else:
            if p == True:
                q = i
                p = False
        if e != -1 and q != -1:
            if c > nb_pixel_min:
                l.append(box.topleft.add(Point(e, 0)))
                l.append(c)
            c = 0
            e = -1
            q = -1
    return l
