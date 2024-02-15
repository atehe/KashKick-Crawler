from utils import clean, click, create_browser, unlimited_scroll, wait_for
from selenium.webdriver.common.by import By
import time
import selenium
from database import conn, insert_data
from datetime import datetime
from logger import logger
from redirects import resolve_redirects
from env import CHECK_REDIRECTS, KASHKICK_EMAIL, KASHKICK_PASSWORD
import random


def get_nested_text(xpath, tag="*"):
    elements = driver.find_elements(by=By.XPATH, value=f"{xpath}/{tag}")

    full_text_list = []

    for element in elements:
        text = element.text
        full_text_list.append(text)

    return " | ".join([word for word in full_text_list if word])


def scrape_offers(driver, spid, offer_type, page_num):
    try:
        logger.info(f"Crawling {offer_type} for id: {spid}")

        driver.get(f"https://kashkick.com/sub/{offer_type}")

        wait_for(
            driver,
            '//div[contains(@class,"offer-block")][@data-offer-id]',
            clickable=True,
            timer=10,
        )

        unlimited_scroll(driver)

        offers = driver.find_elements(
            by=By.XPATH, value='//div[contains(@class,"offer-block")][@data-offer-id]'
        )

        logger.info(f"Found {len(offers)} offers in {offer_type}")
        for i, offer in enumerate(offers):
            try:
                logger.info(f"Parsing {i + 1} in {offer_type}")
                click(driver, offer)

                try:
                    additional = wait_for(
                        driver,
                        ' (//div[contains(@class,"show")] //div[@class="modal-dialog"]//div[contains(@class,"modal-body")])[1]//div[@class="detail-content"]/div[@class="accordion"]',
                        clickable=True,
                    )
                    click(driver, additional)
                except Exception:
                    pass

                title = (
                    offers[i]
                    .find_element(
                        by=By.XPATH,
                        value='.//div[@class="detail-points"]//following-sibling::p',
                    )
                    .text
                )

                try:
                    header_title = (
                        offers[i]
                        .find_element(
                            by=By.XPATH,
                            value='.//span[@class="offer-title"]',
                        )
                        .text
                    )
                except selenium.common.exceptions.NoSuchElementException:
                    header_title = ""

                if header_title:
                    title = f"{header_title}: {title}"

                earn = clean(
                    (
                        offers[i]
                        .find_element(
                            by=By.XPATH,
                            value='.//a[@class="offer-block__bottom__button"]',
                        )
                        .text
                    ),
                    text_to_remove=["Earn", "$"],
                )
                start_url = (
                    offers[i]
                    .find_element(
                        by=By.XPATH,
                        value='.//a[@class="offer-block__bottom__button-link"]',
                    )
                    .get_attribute("href")
                )

                key_points = driver.find_elements(
                    by=By.XPATH,
                    value='(//div[contains(@class,"show")] //div[@class="modal-dialog"]//div[contains(@class,"modal-body")])[1]//div[@class="detail-points"]//div',
                )

                additional_info = get_nested_text(
                    ' (//div[contains(@class,"show")] //div[@class="modal-dialog"]//div[contains(@class,"modal-body")])[1]//div[@class="detail-content"]/div[@class="accordion"]//div',
                )

                try:
                    advice_text = get_nested_text(
                        '(//div[contains(@class,"show")] //div[@class="modal-dialog"]//div[contains(@class,"modal-body")])[1]//div[@class="detail-content"]/div[@class="detail-text"]',
                        tag="/strong",
                    )
                except Exception:
                    advice_text = ""

                detail_text = get_nested_text(
                    '(//div[contains(@class,"show")] //div[@class="modal-dialog"]//div[contains(@class,"modal-body")])[1]//div[@class="detail-content"]/div[@class="detail-text"]',
                )
                offer_data = insert_data(
                    conn,
                    "offerdatas",
                    {
                        "spid": spid,
                        "pagenum": page_num,
                        "title": title,
                        "starturl": start_url,
                        "ordinal": i + 1,
                        "urlfinal": "",
                        "checkedredirects": 0,
                        "reward": earn,
                        "additionalinfo": additional_info,
                        "advicetext": advice_text,
                        "detailtext": detail_text,
                    },
                )

                osid = offer_data.get("osid", random.randint(31, 100))
                logger.debug(f"Scraped offer data spid {spid} - {osid}: {title} ")

                for k_ordinal, key_point in enumerate(key_points):
                    point_text = key_point.text

                    insert_data(
                        conn,
                        "offerdatakeypoints",
                        {
                            "osid": osid,
                            "ordinal": k_ordinal + 1,
                            "pointtext": point_text,
                        },
                    )
                    logger.debug(f"Scraped offer data {osid}: {point_text} ")
            except Exception as e:
                logger.warning(
                    f"Error: {e} while parsing offer {i} of {offer_type} = {spid}"
                )

        logger.info(f"Crawling {offer_type} for id: {spid} finished")
    except Exception as e:
        logger.warn(f"Error: {e} in {spid} of {offer}")


def login(driver):
    logger.info("Sign in into to KASHKICK")
    driver.get("https://kashkick.com/login")

    time.sleep(1)

    email_input = wait_for(driver, xpath='//input[@name="Email"]')
    email_input.send_keys(KASHKICK_EMAIL)

    time.sleep(1)

    password_input = wait_for(driver, xpath='//input[@name="Password"]')
    password_input.send_keys(KASHKICK_PASSWORD)

    time.sleep(1)

    submit_button = wait_for(driver, xpath='//button[@name="Login"]', clickable=True)

    click(driver, submit_button)

    time.sleep(1)

    logger.info("Sign in complete")


if __name__ == "__main__":
    driver = create_browser(headless=False)

    login(driver)

    # When the program starts spidering https://kashkick.com
    # it should create an entry in the spiderings table with a website field value of “kashkick”.
    spiderring_data = insert_data(
        conn,
        "spiderings",
        {
            "spiderstart": str(datetime.now().strftime("%d/%m/%y %H:%M:%S")),
            "website": "kashkick",
        },
    )
    spid = spiderring_data.get("spid", random.randint(31, 1000))

    scrape_offers(driver, spid, "games", 1)
    scrape_offers(driver, spid, "offers", 2)

    if CHECK_REDIRECTS:

        resolve_redirects(driver)

    logger.info(f"Finished crawling Kashkick - {spid}")
    driver.quit()
