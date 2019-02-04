import io
import os, datetime, time
import numpy as np
import cv2
import pytesseract

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import Configs
import ImageAnalyser as ia
import BotEngine as be
import LaunchZombidle as lz

import logging
from logging.handlers import RotatingFileHandler

def getTimeNow():
    return datetime.datetime.now().strftime("%Y.%m.%d_%H.%M.%S.%f")

if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger("ZombidleBotLogger")
logger.setLevel(logging.DEBUG)
now = datetime.datetime.now()
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('logs/'+str(getTimeNow())+'.log', maxBytes=10000000)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

screenShotFolder = "screenshots"

def takeScreenshot(driver):
    el = driver.find_element(By.ID, 'zigame')
    if not os.path.exists(screenShotFolder):
        os.makedirs(screenShotFolder)
    el.screenshot(screenShotFolder + "/screenshot_" + str(getTimeNow()) + ".png")

def autoclick(driver, zg, configs):
    logger.info("Autoclick start")
    move = ActionChains(driver)
    move.move_to_element_with_offset(zg, configs.clickPos[0], configs.clickPos[1])
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
    logger.info("Autoclick end")

def click(driver, zg, x, y):
    logger.info("Click at (" + str(x) + "," + str(y) + ")")
    a = ActionChains(driver)
    a.move_to_element_with_offset(zg, x, y)
    a.click_and_hold()
    a.pause(1)
    a.release()
    a.perform()

def saveItemNotif(driver, name, configs, pos=1):
    el = driver.find_element(By.ID, 'zigame')
    arr = np.fromstring(el.screenshot_as_png, np.uint8)
    img = cv2.imdecode(arr, 1)
    crop_img = img[configs.notifPos[1] : configs.notifPos[1] + configs.notifSize[1],
        configs.notifPos[0] + configs.notifDeplaSize[0] * (pos - 1) : configs.notifPos[0] + configs.notifSize[0] + configs.notifDeplaSize[0] * (pos - 1)].copy()
    cv2.imwrite(name, crop_img)

def saveScreenPart(driver, name, box):
    el = driver.find_element(By.ID, 'zigame')
    arr = np.fromstring(el.screenshot_as_png, np.uint8)
    img = cv2.imdecode(arr, 1)
    cv2.imwrite(name, img[box[1]:box[3], box[0]:box[2]])

def saveGoToArcaneButton(driver, configs):
    saveScreenPart(driver, "GoToArcaneButton.png", configs.goToArcaneBox)

def saveArcaneIMG(driver, configs):
    saveScreenPart(driver, "ArcaneIMG.png", configs.arcaneIMGBox)

def takeAction(driver, zg, configs):
    arr = np.fromstring(zg.screenshot_as_png, np.uint8)
    img = cv2.imdecode(arr, 0)

    action  = be.determineAction(img, configs)
    if action[0] == 1 or action[0] == 2 or action[0] == 7 or action[0] == 4:
        click(driver, zg, action[1], action[2])
    if action[0] == 3:
        r = be.processDeal(img, configs)
        click(driver, zg, r[0], r[1])
    if action[0] == 5:
        r = be.processArcane(img, configs)
        click(driver, zg, r[0], r[1])
    if action[0] == 6:
        autoclick(driver, zg, configs)



def run(driver, it=10):
    logger.info("Run")
    zg = driver.find_element(By.ID, 'zigame')
    configs = Configs.Configs()
    for i in range(it):
        takeAction(driver, zg, configs)
        time.sleep(1)



def main():
    driver = lz.openBrowser()
    lz.launchZombidle(driver)
    run(driver)
    return driver



if __name__ == "__main__":
    # execute only if run as a script
    driver = main()
