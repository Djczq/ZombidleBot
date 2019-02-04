import cv2
import pytesseract

def findTemplateInImage(img, template):
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF)
    w, h = template.shape[::-1]
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return (max_loc[0], max_loc[1], max_loc[0] + w, max_loc[1] + h)

def isInside(boxIn, boxOut):
    """check if boxIn is inside boxOut"""
    if boxIn[0] < boxOut[0] or boxIn[0] > boxOut[2]:
        return False
    if boxIn[2] < boxOut[0] or boxIn[2] > boxOut[2]:
        return False
    if boxIn[1] < boxOut[1] or boxIn[1] > boxOut[3]:
        return False
    if boxIn[3] < boxOut[1] or boxIn[3] > boxOut[3]:
        return False
    return True

def readCharacters(img, box):
    return pytesseract.image_to_string(img[box[1]:box[3], box[0]:box[2]]).replace("\n", "").replace("\r", "")

