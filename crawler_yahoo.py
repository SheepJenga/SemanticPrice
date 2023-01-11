import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import datetime
import random
import sqlite3
import re

def main():
    # Establish connection to Database
    con = sqlite3.connect("ticker_info.db")
    cur = con.cursor()

    curr_date = datetime.date.today().isoformat()
    tickers = ["TSLA", "MSFT", "AMZN", "AAPL", "GOOGL", "NVDA", "META", "IBM"]
    companies = ["tesla", "microsoft", "amazon", "apple", "google", "nvidia", "meta", "IBM"]
    user_agent = UserAgent()
    max_page = 5

    for company, ticker in zip(companies, tickers):
        page = 1
        error_counter = 0
        while page <= max_page:
            headers = {'User-Agent': user_agent.random, 'Referer': "https://www.google.com/"}
            URL = f"https://news.search.yahoo.com/search?p={company}&fr2=piv-web&b={page-1}1&pz=10&bct=0&xargs=0"

            resp = requests.get(URL, headers=headers)
            while resp.status_code != 200:
                time.sleep(random.random()*1.5 + 1)
                resp = requests.get(URL, headers=headers)
            time.sleep(random.random()*1.5 + 1)
            soup = BeautifulSoup(resp.content, 'html5lib')
            headline_table = soup.find_all('a', attrs={'style': "font-size:16px;"})
            data = [(ticker, 'yahoo', curr_date, row.text) for row in headline_table]
            # print(data)

            if not data and error_counter < 5:
                error_counter += 1
                continue
            error_counter = 0

            cur.executemany("INSERT INTO all_headlines VALUES(?, ?, ?, ?)", data)
            con.commit()
            page += 1

    con.close()

if __name__ == "__main__":
    main()
