# KashKick-Crawler

Scripts to crawl https://kashkick.com to a MSSQL server DB

### USAGE

To run the script rename the `.env.example` to `.env` and set the required variables in it

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
