from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
import undetected_chromedriver as uc
import re
import time
from env import HEAD_MODE, USERAGENT, CHROME_VER
from logger import logger


def clean(string, text_to_remove=[]):
    if isinstance(string, list):
        string = " ".join(string)

    if not string:
        return string

    string = str(string)
    string = string.replace("\r", "").replace("\\r", "")
    string = string.replace("\n", "").replace("\\n", "")
    string = string.replace("\t", "").replace("\\t", "")
    string = re.sub(r"\s+", " ", string)

    for text in text_to_remove:
        string = re.sub(rf"{text}", "", string)

    string = string.strip()
    return string


def click(driver, element):
    """Use javascript click if selenium click method fails"""
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)


def create_browser(headless=HEAD_MODE):
    user_agent = USERAGENT
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={user_agent}")

    driver = uc.Chrome(options=options, version_main=CHROME_VER)
    logger.info("Launched undetectable browser")
    return driver


def wait_for(driver, xpath, clickable=False, timer=5):
    wait = WebDriverWait(driver, timer)

    try:
        if clickable:
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        else:
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        return element
    except TimeoutException:
        logger.debug(f"Element not found: {xpath}")


def unlimited_scroll(driver, pause_time=5):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height
