import time
import datetime
import os
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def getTimeNow():
    return datetime.datetime.now().strftime("%Y.%m.%d_%H.%M.%S.%f")

logger = logging.getLogger("ZombidleBotLogger")
screenShotFolder = "screenshots"

class SeleniumHook:
    def __init__(self, driver):
        self.driver = driver
        self.zg = self.driver.find_element(By.ID, 'zigame')

    def takeScreenshot(self):
        if not os.path.exists(screenShotFolder):
            os.makedirs(screenShotFolder)
        self.zg.screenshot(screenShotFolder + "/screenshot_" + str(getTimeNow()) + ".png")

    def press0(self):
        logger.info("Activate Skills (press 0)")
        self.zg = self.driver.find_element(By.ID, 'zigame')
        self.zg.click()
        self.zg.send_keys("00000")
        return
        a = ActionChains(self.driver)
        a.key_down(Keys.NUMPAD0, self.zg)
        a.pause(0.8)
        a.key_up(Keys.NUMPAD0, self.zg)
        a.perform()

    def autoclick(self, settings):
        logger.info("Autoclick start")
        move = ActionChains(self.driver)
        move.move_to_element_with_offset(self.zg, settings.clickPos.width, settings.clickPos.height)
        move.perform()
        c = ActionChains(self.driver)
        c.click_and_hold()
        c.pause(0.1)
        c.release()
        for i in range(100):
            c.perform()
            time.sleep(0.2)
            if i % 20 == 0:
                move.perform()
        logger.info("Autoclick end")

    def click(self, pos):
        logger.info("Click at " + str(pos))
        a = ActionChains(self.driver)
        a.move_to_element_with_offset(self.zg, pos.width, pos.height)
        a.click_and_hold()
        a.pause(1)
        a.release()
        a.perform()
