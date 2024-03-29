import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(".env")


# browser settings
HEAD_MODE = bool(int(os.environ.get("HEADLESS")))
USERAGENT = os.environ.get("USERAGENT")
CHROME_VER = os.environ.get("CHROME_VER")
PROXY_FILE = os.environ.get("PROXY_FILE")


# database settings
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")


# logging settings
LOG_FILE = os.environ.get("LOG_FILE")
QUERY_LOG_FILE = os.environ.get("QUERY_LOG_FILE")


# kashskick setting
KASHKICK_EMAIL = os.environ.get("KASHKICK_EMAIL")
KASHKICK_PASSWORD = os.environ.get("KASHKICK_PASSWORD")


CHECK_REDIRECTS = bool(int(os.environ.get("CHECK_REDIRECTS")))

if __name__ == "__main__":
    print(
        "Loading ENV: ",
        str(
            {
                "HEAD_MODE": HEAD_MODE,
                "USERAGENT": USERAGENT,
                "DB_NAME": DB_NAME,
                "DB_USER": DB_USER,
                "DB_PASS": DB_PASS,
                "DB_PORT": DB_PORT,
                "DB_HOST": DB_HOST,
                "LOG_FILE": LOG_FILE,
                "KASHKICK_EMAIL": KASHKICK_EMAIL,
                "KASHKICK_PASSWORD": KASHKICK_PASSWORD,
                "QUERY_LOG_FILE": QUERY_LOG_FILE,
                "CHROME_VER": CHROME_VER,
                "PROXY_FILE": PROXY_FILE,
                "CHECK_REDIRECTS": CHECK_REDIRECTS,
            }
        ),
    )
