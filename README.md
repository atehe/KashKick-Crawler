# KashKick-Crawler

Scripts to crawl https://kashkick.com to a MSSQL server DB

## REQUIREMENTS AND INSTALLATION

The following are bas requirement that the crawler needs to run

- Python
- Chrome Browser

Once this has been met other requirements like the python libraries the crawler needs can be installed using

```
cd KashKick-Crawler
pip install requirements.txt
```

Key variables that the crawler needs are set in the `.env` file.
This can be seen in the `.env.example` file.
To set the variables, rename `env.example` to `.env` and fill accordingly

- `HEADLESS`: Sets the browser to show while crawling. `0` makes it show while `1` disables it
- `KASHKICK_EMAIL`: Login email for the website
- `KASHKICK_PASSWORD`: Login password
- `LOG_FILE`: File path where the log should be stored
- `USERAGENT`: Mobile User Agent for the browser
- `DB_HOST`: SQL server host
- `DB_PASS`: SQL server password
- `DB_USER`: SQL sever user
- `DB_NAME`: Database Name
- `DB_PORT`: SQL server PORT
- `QUERY_LOG_FILE`: Logs queries that saves data to the server
- `CHROME_VER`: Version of chrome installed

### USAGE

To run the script

```
python3 kashskick.py
```
