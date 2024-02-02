from database import execute_query, insert_data, conn, update_data
from logger import logger


def get_redirects(driver, url):
    driver.get(url)
    final_url = driver.current_url

    redirects = []  # todo: get redirects
    return [url] + redirects + [final_url]


def check_redirects(driver, url, osid):
    logger.info(f" Getting redirects for {osid}, {url}")

    redirects = get_redirects(driver, url)
    for ordinal, redirect in enumerate(redirects):
        insert_data(
            conn,
            "offerdataredirects",
            {"osid": osid, "ordinal": ordinal, "url": redirect},
        )
        print(redirect)

        if ordinal == len(redirects) - 1:
            # update offerdata final url
            update_data(
                conn,
                "offerdata",
                {"urlfinal": redirect, "checkedredirects": 1},
                {"osid": osid},
            )


def resolve_redirects(driver):
    # get redirects url and osid not checked from offers table
    data = execute_query(conn, "select * from offerdata where checkedredirects = 0")

    for offerdata in data:
        osid = offerdata.get("osid")
        start_url = offerdata.get("starturl")

        check_redirects(driver, start_url, osid)
