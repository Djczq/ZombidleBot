import io
import os, datetime, time
import numpy as np
import cv2
import pytesseract

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


screenShotFolder = "screenshots"

# coord : (width = left-->rigth (x), heigh = top-->bottom (y))
# box : (top-left width, top-left heigh, bottom-rigth width, bottom-rigth heigh)
notifDeplaSize=(65, 0)
notifSize=(24, 24)
notifPos=(90, 30)
notifBox=(74, 9, 440, 72)

itemTabPos=(810, 140)

clickPos = (155, 333)

goToArcaneBox = (824, 234, 900, 287)
arcaneIMGBox = (745, 12, 770, 80)
goToArcanePos = (860, 260)
arcaneTimerBox = (834, 66, 938, 92)
arcaneQuitPos = (914, 46)

nextBoostPos = (196, 130)
collectAllPos = (377, 130)
fastGhostCraftPos = (600, 130)
repeatLastCraftPos = (812, 130)

dealBox = (560, 80, 700, 110)
dealThanksBox = (440, 108, 516, 129)
dealContentBox = (410, 180, 852, 376)
dealAwsomeBox = (732, 445, 828, 467)
dealAwsomePos = (777, 455)
dealNoPos = (486, 455)
dealYesPos = (650, 455)
dealExitPubPos = (666, 140)

backArrowPos = (75, 575)

def takeScreenshot(driver):
    el = driver.find_element(By.ID, 'zigame')
    now = datetime.datetime.now()
    if not os.path.exists(screenShotFolder):
        os.makedirs(screenShotFolder)
    el.screenshot(screenShotFolder + "/screenshot_" + str(now.isoformat()) + ".png")

def autoclick(driver, zg):
    move = ActionChains(driver)
    move.move_to_element_with_offset(zg, clickPos[0], clickPos[1])
    move.perform()
    click = ActionChains(driver)
    click.click_and_hold()
    click.pause(0.1)
    click.release()
    for i in range(100):
        click.perform()
        time.sleep(0.2)
        if i % 20 == 0:
            move.perform()

def click(driver, zg, x, y):
    a = ActionChains(driver)
    a.move_to_element_with_offset(zg, x, y)
    a.click_and_hold()
    a.pause(1)
    a.release()
    a.perform()

def saveItemNotif(driver, name, pos=1):
    el = driver.find_element(By.ID, 'zigame')
    arr = np.fromstring(el.screenshot_as_png, np.uint8)
    img = cv2.imdecode(arr, 1)
    crop_img = img[notifPos[1] : notifPos[1] + notifSize[1], notifPos[0] + notifDeplaSize[0] * (pos - 1) : notifPos[0] + notifSize[0] + notifDeplaSize[0] * (pos - 1)].copy()
    cv2.imwrite(name, crop_img)

def saveScreenPart(driver, name, box):
    el = driver.find_element(By.ID, 'zigame')
    arr = np.fromstring(el.screenshot_as_png, np.uint8)
    img = cv2.imdecode(arr, 1)
    cv2.imwrite(name, img[box[1]:box[3], box[0]:box[2]])

def saveGoToArcaneButton(driver):
    saveScreenPart(driver, "GoToArcaneButton.png", goToArcaneBox)

def saveArcaneIMG(driver):
    saveScreenPart(driver, "ArcaneIMG.png", arcaneIMGBox)

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
    return pytesseract.image_to_string(img[box[1]:box[3], box[0]:box[2]])

def processDeal(img):
    read = readCharacters(img, dealContentBox)
    if "Skull" in read or "damage" in read or "chest" in read or "minutes" in read:
        return (dealNoPos[0], dealNoPos[1])
    if "sec" in read and "nds" in read:
        return (dealNoPos[0], dealNoPos[1])
    if "x" in read or "craft" in read or "time" in read:
        if "free" in read:
            return (dealAwsomePos[0], dealAwsomePos[1])
        else:
            return (dealYesPos[0], dealYesPos[1])
    return (dealNoPos[0], dealNoPos[1])

def processArcane(img):
    if img[collectAllPos[1], collectAllPos[0]] > 55:
        return (collectAllPos[0], collectAllPos[1])
    if img[repeatLastCraftPos[1], repeatLastCraftPos[0]] > 55:
        return (repeatLastCraftPos[0], repeatLastCraftPos[1])
    if img[fastGhostCraftPos[1], fastGhostCraftPos[0]] > 55:
        return (fastGhostCraftPos[0], fastGhostCraftPos[1])
    if img[nextBoostPos[1], nextBoostPos[0]] > 55:
        return (nextBoostPos[0], nextBoostPos[1])
    return (arcaneQuitPos[0], arcaneQuitPos[1])

def goToArcane(driver, zg, img):
    template = cv2.imread("GoToArcaneButton.png", 0)
    res = findTemplateInImage(img, template)
    if isInside(res, goToArcaneBox):
        click(driver, zg, goToArcanePos[0], goToArcanePos[1])
    else:
        click(driver, zg, itemTabPos[0], itemTabPos[1])
    
def determineAction(img):
    read = readCharacters(img, dealBox)
    if read == "THE DEAL":
        return (3, )

    read = readCharacters(img, dealThanksBox)
    if read == "Thanks!":
        return (7, dealExitPubPos[0], dealExitPubPos[1])

    template = cv2.imread("ArcaneIMG.png", 0)
    res = findTemplateInImage(img, template)
    if isInside(res, arcaneIMGBox):
        return (5, )

    template = cv2.imread("Scroll.png", 0)
    res = findTemplateInImage(img, template)
    if isInside(res, notifBox):
        return (1, (res[0] + res[2]) / 2, (res[1] + res[3]) / 2)
    template = cv2.imread("ChestCollector.png", 0)
    res = findTemplateInImage(img, template)
    if isInside(res, notifBox):
        return (2, (res[0] + res[2]) / 2, (res[1] + res[3]) / 2)

    read = readCharacters(img, arcaneTimerBox)
    if "A" in read:
        return (4, )

    print img[backArrowPos[1], backArrowPos[0]]
    if img[backArrowPos[1], backArrowPos[0]] == 211:
        return (6, )
    return (0, )


def takeAction(driver, zg):
    arr = np.fromstring(zg.screenshot_as_png, np.uint8)
    img = cv2.imdecode(arr, 0)

    action  = determineAction(img)
    if action[0] == 1 or action[0] == 2 or action[0] == 7:
        click(driver, zg, action[1], action[2])
    if action[0] == 3:
        r = processDeal(img)
        click(driver, zg, r[0], r[1])
    if action[0] == 4:
        goToArcane(driver, zg, img)
    if action[0] == 5:
        r = processArcane(img)
        click(driver, zg, r[0], r[1])
    if action[0] == 6:
        autoclick(driver, zg)



def run(driver, it=10):
    zg = driver.find_element(By.ID, 'zigame')
    for i in range(it):
        takeAction(driver, zg)
        time.sleep(1)



