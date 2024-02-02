from utils import clean, click, create_browser, unlimited_scroll, wait_for
from selenium.webdriver.common.by import By
import time
import selenium
from database import conn, insert_data
from datetime import datetime
from logger import logger
from redirects import resolve_redirects
from env import KASHKICK_EMAIL, KASHKICK_PASSWORD


def scrape_offers(driver, spid, offer_type, page_num):
    logger.info(f"Crawling {offer_type} for {spid}")

    driver.get(f"https://kashkick.com/sub/{offer_type}")

    unlimited_scroll(driver)

    offers = driver.find_elements(
        by=By.XPATH, value='//div[contains(@class,"offer-block")][@data-offer-id]'
    )

    for i, offer in enumerate(offers):
        click(driver, offer)

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
            value='//div[@class="modal-dialog"]//div[@class="detail-points"]//div',
        )

        additional_info = driver.find_element(
            by=By.XPATH,
            value=' //div[@class="modal-dialog"]//div[@class="detail-content"]/div[@class="accordion"]',
        ).text
        advice_text = driver.find_element(
            by=By.XPATH,
            value='//div[@class="modal-dialog"]//div[@class="detail-content"]/div[@class="detail-text"]//strong',
        ).text
        detail_text = driver.find_element(
            by=By.XPATH,
            value='//div[@class="modal-dialog"]//div[@class="detail-content"]/div[@class="detail-text"]',
        ).text

        offer_data = insert_data(
            conn,
            "offerdata",
            {
                "spid": spid,
                "pagenum": page_num,
                "title": title,
                "starturl": start_url,
                "urlfinal": "",
                "checkedredirects": 0,
                "reward": earn,
                "additionalinfo": additional_info,
                "advicetext": advice_text,
                "detailtext": detail_text,
            },
        )

        osid = offer_data.get("osid")
        logger.debug(f"Scraped offer data {osid}: {title} ")

        for ordinal, key_point in enumerate(key_points):
            point_text = key_point.text

            insert_data(
                conn,
                "offerdatakeypoints",
                {"osid": osid, "ordinal": ordinal + 1, "pointtext": point_text},
            )
            logger.debug(f"Scraped offer data {osid}: {point_text} ")

    logger.info(f"Crawling {offer_type} for {spid} finished")


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
        "spiderrings",
        {
            "spiderstart": str(datetime.now().strftime("%d/%m/%y %H:%M:%S")),
            "website": "kashkick",
        },
    )
    spid = spiderring_data.get("spid")

    scrape_offers(driver, spid, "games", 1)
    scrape_offers(driver, spid, "offers", 2)

    resolve_redirects(driver)

    logger.info(f"Finished crawling Kashkick - {spid}")
    driver.quit()
