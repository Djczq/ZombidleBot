import io, sys
import os, datetime, time
import numpy as np
import cv2
import pytesseract

import ZombidleBot.settings.Settings as bs
import ZombidleBot.ImageAnalyser as ia
import ZombidleBot.BotEngine as be
import ZombidleBot.LaunchZombidle as lz
import ZombidleBot.Hook as hk

import importlib

import logging
from logging.handlers import RotatingFileHandler

from multiprocessing import Process, Pipe

def reloadModules():
    importlib.reload(ia)
    importlib.reload(be)
    importlib.reload(lz)
    importlib.reload(bs)
    importlib.reload(hk)
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

def takeAction(hook, settings):
    arr = np.fromstring(hook.zg.screenshot_as_png, np.uint8)
    img = cv2.imdecode(arr, 0)

    action = be.determineAction(img, settings)
    if action[0] == 1:
        hook.click(action[1])
    if action[0] == 4:
        hook.press0()
        hook.autoclick(settings)

def botProcess(conn, driver):
    logger.info("Start bot process")
    settings = bs.Settings()
    hook = hk.SeleniumHook(driver)
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
                hook.takeScreenshot()
            if r == "reload":
                reloadModules()
                settings = bs.Settings()
                hook = hk.SeleniumHook(driver)
        if run:
            try:
                takeAction(hook, settings)
            except:
                logger.warn(sys.exc_info())
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
