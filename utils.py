from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
import requests
import undetected_chromedriver as uc
import re
import time
from env import HEAD_MODE, USE_PROXY, USERAGENT, CHROME_VER, PROXY_LIST
from logger import logger
import os
import random
from seleniumwire import webdriver

import chromedriver_binary  # noqa: F401

PROXY_FILE = "proxy.txt"


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
    string = string.replace("'", "").replace('"', "")
    # string = string.encode("ascii", "ignore").decode("ascii")

    for text in text_to_remove:
        string = string.replace(f"{text}", "")

    string = string.strip()
    return string


def click(driver, element):
    """Use javascript click if selenium click method fails"""
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)


def create_browser(headless=HEAD_MODE, use_proxy=USE_PROXY):
    user_agent = USERAGENT
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={user_agent}")

    if use_proxy:
        proxy = get_proxy()
        proxy_server, port, userame, password = proxy.split(":")
        seleniumwire_options = {
            "proxy": {
                "https": f"https://{userame}:{password}@{proxy_server}:{port}",
                "http": f"https://{userame}:{password}@{proxy_server}:{port}",
                "no_proxy": "localhost,127.0.0.1",  # excludes
            }
        }
        driver = webdriver.Chrome(
            options=options,
            seleniumwire_options=seleniumwire_options,
        )
        logger.info("Launched Proxy browser")
        return driver

    driver = uc.Chrome(options=options, version_main=int(CHROME_VER))
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
    logger.debug("Scrolling down to the end of page....")
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


def download_file(url, destination):
    print("Downloading...")
    response = requests.get(url)

    if response.status_code == 200:
        with open(destination, "wb") as file:
            file.write(response.content)
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")


def get_proxy():

    if not os.path.exists(PROXY_FILE):

        download_file(
            PROXY_LIST,
            PROXY_FILE,
        )

    proxy_list = [proxy for proxy in open(PROXY_FILE).read().split("\n") if proxy]
    selected_proxy = random.choice(proxy_list)
    logger.info(f"Selected proxy: {selected_proxy}")

    return selected_proxy
