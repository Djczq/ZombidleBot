import cv2
import pytesseract
from settings.Rectangle import Rectangle

def findTemplateInImage(img, template):
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF)
    w, h = template.shape[::-1]
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return Rectangle.fromValues(max_loc[0], max_loc[1], max_loc[0] + w, max_loc[1] + h)

def readCharacters(img, box):
    return pytesseract.image_to_string(img[box.getSliceNP()]).replace("\n", "").replace("\r", "")

