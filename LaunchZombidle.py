from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

def openBrowser():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--user-data-dir=./profile")
    driver = webdriver.Chrome(options=options)
    return driver


def changeSiteSettings(driver, site, setting, value):
    driver.get("chrome://settings/content/siteDetails?site=" + site)
    time.sleep(1)
    root1 = driver.find_element(By.TAG_NAME, "settings-ui")
    shadowRoot1 = driver.execute_script("return arguments[0].shadowRoot", root1)
    root2 = shadowRoot1.find_element(By.ID, "container")
    main = root2.find_element(By.ID, "main")
    shadowRoot3 = driver.execute_script("return arguments[0].shadowRoot", main)
    shadowRoot4 = shadowRoot3.find_element(By.CLASS_NAME, "showing-subpage")
    shadowRoot5 = driver.execute_script("return arguments[0].shadowRoot", shadowRoot4)
    shadowRoot6 = shadowRoot5.find_element(By.ID, "advancedPage")
    shadowRoot7 = shadowRoot6.find_element(By.TAG_NAME, "settings-privacy-page")
    shadowRoot8 = driver.execute_script("return arguments[0].shadowRoot", shadowRoot7)
    shadowRoot9 = shadowRoot8.find_element(By.ID, "pages")
    shadowRoot10 = shadowRoot9.find_element(By.TAG_NAME, "settings-subpage")
    shadowRoot11= shadowRoot10.find_element(By.TAG_NAME, "site-details")
    shadowRoot12 = driver.execute_script("return arguments[0].shadowRoot", shadowRoot11)
    shadowRoot13 = shadowRoot12.find_element(By.ID, setting)
    shadowRoot14 = driver.execute_script("return arguments[0].shadowRoot", shadowRoot13)
    #allow block ask default
    Select(shadowRoot14.find_element(By.ID, "permission")).select_by_value(value)


def launchZombidle(driver):
    site = "http://www.zombidle.com/"
    changeSiteSettings(driver, site, "plugins", "allow")
    changeSiteSettings(driver, site, "automaticDownloads", "allow")
    driver.get(site)

