import io
import os, datetime, time
import numpy as np
import cv2
import pytesseract

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import ZombidleBot.settings.Settings as bs
import ZombidleBot.ImageAnalyser as ia
import ZombidleBot.BotEngine as be
import ZombidleBot.LaunchZombidle as lz

import importlib

import logging
from logging.handlers import RotatingFileHandler

from multiprocessing import Process, Pipe

def reloadModules():
    importlib.reload(ia)
    importlib.reload(be)
    importlib.reload(lz)
    be.reloadModules()

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

def takeScreenshot(el):
    if not os.path.exists(screenShotFolder):
        os.makedirs(screenShotFolder)
    el.screenshot(screenShotFolder + "/screenshot_" + str(getTimeNow()) + ".png")

def autoclick(driver, zg, settings):
    logger.info("Autoclick start")
    move = ActionChains(driver)
    move.move_to_element_with_offset(zg, settings.clickPos.width, settings.clickPos.height)
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

def click(driver, zg, pos):
    logger.info("Click at " + str(pos))
    a = ActionChains(driver)
    a.move_to_element_with_offset(zg, pos.width, pos.height)
    a.click_and_hold()
    a.pause(1)
    a.release()
    a.perform()

def takeAction(driver, zg, settings):
    arr = np.fromstring(zg.screenshot_as_png, np.uint8)
    img = cv2.imdecode(arr, 0)

    action  = be.determineAction(img, settings)
    if action[0] == 1:
        click(driver, zg, action[1])
    if action[0] == 4:
        autoclick(driver, zg, settings)


def botProcess(conn, driver):
    logger.info("Start bot process")
    zg = driver.find_element(By.ID, 'zigame')
    settings = bs.Settings()
    run = True
    while True:
        if conn.poll():
            r = conn.recv()
            logger.info("Bot process receveid :" + r)
            if r == "stop":
                run = False
            if r == "start":
                run = True
            if r == "quit":
                break
            if r == "screenshot" or r == "capture" or r == "cap":
                takeScreenshot(zg)
            if r == "reload":
                reloadModules()
                settings = bs.Settings()
        if run:
            takeAction(driver, zg, settings)
    logger.info("Stop bot process")
    conn.close()

def main():
    driver = lz.openBrowser()
    lz.launchZombidle(driver)
    parent_conn, child_conn = Pipe()
    p = Process(target=botProcess, args=(child_conn, driver))
    p.start()
    step = ""
    while step != "quit":
        print("step ? stop start quit")
        step = input()
        if len(step) > 0:
            parent_conn.send(step)
    parent_conn.send("quit")
    p.join()
    driver.quit()


if __name__ == "__main__":
    main()
