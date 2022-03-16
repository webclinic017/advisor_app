import warnings
from finvizfinance.quote import finvizfinance
import yfinance as yf
from yahooquery import Ticker
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import finviz
from os.path import exists

from src.data.source_data import Source_Data
import src.data.yahoo_fin_stock_info as si
from src.tools.functions import company_longName

warnings.filterwarnings("ignore")
pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.width = None
pd.options.display.float_format = "{:,}".format
nltk.download("vader_lexicon")


class Recommendations3(object):

  # Parameters
    def __init__(self, today=str(datetime.now())[:10]):
        self.today_stamp = today
        self.saveMonth = str(datetime.now())[:7]
        self.saveDay = str(datetime.now())[8:10]

        self.saveRec = Path(f"data/recommenders/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveRec.exists():
            self.saveRec.mkdir(parents=True)

        self.saveRaw = Path(f"data/raw/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveRaw.exists():
            self.saveRaw.mkdir(parents=True)

        self.saveScreeners = Path(f"data/screeners/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveScreeners.exists():
            self.saveScreeners.mkdir(parents=True)

        self.saveTickers = Path(f"data/tickers/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveTickers.exists():
            self.saveTickers.mkdir(parents=True)


  # Get Data
    def run_rec3(self):
        if exists(self.saveRec / f"recommender_03_return_dataFrame.pkl"):
            return
        elif not exists(self.saveRec / f"recommender_02_return_dataFrame.pkl"):
            print("* * * [ERROR] NO FILE FOUND FOR RECOMMENDER 1 * * *")
        else:
            symbols = list(pd.read_pickle(self.saveRec / f"recommender_02_return_dataFrame.pkl")["Symbol"])

        self.n = 3
        self.tickers = symbols
        finwiz_url = "https://finviz.com/quote.ashx?t="
        news_tables = {}
        print(f"\n - - - Resulting Ticker List Length = {len(self.tickers)} - - -\n")

        for ticker in self.tickers:
            url = finwiz_url + ticker
            req = Request(url=url, headers={"user-agent": "my-app/0.0.1"})
            resp = urlopen(req)
            html = BeautifulSoup(resp, features="lxml")
            news_table = html.find(id="news-table")
            news_tables[ticker] = news_table

        remove_pile = []
        for ticker in self.tickers:
            df = news_tables[ticker]
            if df:
                try:
                    df_tr = df.findAll("tr")
                    st.subheader("Recent News Headlines for [{}]: ".format(ticker))
                    for i, table_row in enumerate(df_tr):
                        a_text = table_row.a.text
                        td_text = table_row.td.text
                        td_text = td_text.strip()
                        print("* ", a_text, "(", td_text, ")")
                        if i == self.n - 1:
                            break
                except:
                    remove_pile.append(ticker)
                    print(ticker)
                    pass

        if remove_pile:
            for r in remove_pile:
                self.tickers.remove(r)

      # Iterate through the news
        parsed_news = []
        for file_name, news_table in news_tables.items():
            for x in news_table.findAll("tr"):
                text = x.a.get_text()
                date_scrape = x.td.text.split()
                if len(date_scrape) == 1:
                    time = date_scrape[0]
                else:
                    date = date_scrape[0]
                    time = date_scrape[1]
                ticker = file_name.split("_")[0]
                parsed_news.append([ticker, date, time, text])

      # Sentiment Analysis
        analyzer = SentimentIntensityAnalyzer()
        columns = ["Symbol", "Date", "Time", "Headline"]
        news = pd.DataFrame(parsed_news, columns=columns)
        scores = news["Headline"].apply(analyzer.polarity_scores).tolist()
        df_scores = pd.DataFrame(scores)
        news = news.join(df_scores, rsuffix="_right")

      # View Data
        news["Date"] = pd.to_datetime(news.Date).dt.date
        unique_ticker = news["Symbol"].unique().tolist()
        news_dict = {name: news.loc[news["Symbol"] == name] for name in unique_ticker}
        values = []
        for ticker in self.tickers:
            dataframe = news_dict[ticker]
            dataframe = dataframe.set_index("Symbol")
            dataframe = dataframe.drop(columns=["Headline"])
            mean = round(dataframe["compound"].mean() * 100, 0)
            values.append(mean)


        df = pd.DataFrame(self.tickers, columns=["Symbol"])
        df["Mean Sentiment"] = values
        df = df.sort_values("Mean Sentiment", ascending=False)
        df["rank"] = range(1, len(df.index) + 1)
        df = df.set_index("rank")

        df = df[df["Mean Sentiment"] >= 10]
        df.to_pickle(f"data/recommenders/{self.saveMonth}/{self.today_stamp}/recommender_03_return_dataFrame.pkl")
        return


    def run_rec3_personal_port(self, start_lst):
        self.n = 3
        self.tickers = start_lst
        finwiz_url = "https://finviz.com/quote.ashx?t="
        news_tables = {}
        print(f"\n - - - Resulting Ticker List Length = {len(self.tickers)} - - -\n")

        for ticker in self.tickers:
            url = finwiz_url + ticker
            req = Request(url=url, headers={"user-agent": "my-app/0.0.1"})
            resp = urlopen(req)
            html = BeautifulSoup(resp, features="lxml")
            news_table = html.find(id="news-table")
            news_tables[ticker] = news_table

        remove_pile = []
        for ticker in self.tickers:
            df = news_tables[ticker]
            if df:
                try:
                    df_tr = df.findAll("tr")
                    st.subheader("Recent News Headlines for [{}]: ".format(ticker))
                    for i, table_row in enumerate(df_tr):
                        a_text = table_row.a.text
                        td_text = table_row.td.text
                        td_text = td_text.strip()
                        print("* ", a_text, "(", td_text, ")")
                        if i == self.n - 1:
                            break
                except:
                    remove_pile.append(ticker)
                    print(ticker)
                    pass

        if remove_pile:
            for r in remove_pile:
                self.tickers.remove(r)

      # Iterate through the news
        parsed_news = []
        for file_name, news_table in news_tables.items():
            for x in news_table.findAll("tr"):
                text = x.a.get_text()
                date_scrape = x.td.text.split()
                if len(date_scrape) == 1:
                    time = date_scrape[0]
                else:
                    date = date_scrape[0]
                    time = date_scrape[1]
                ticker = file_name.split("_")[0]
                parsed_news.append([ticker, date, time, text])

      # Sentiment Analysis
        analyzer = SentimentIntensityAnalyzer()
        columns = ["Symbol", "Date", "Time", "Headline"]
        news = pd.DataFrame(parsed_news, columns=columns)
        scores = news["Headline"].apply(analyzer.polarity_scores).tolist()
        df_scores = pd.DataFrame(scores)
        news = news.join(df_scores, rsuffix="_right")

      # View Data
        news["Date"] = pd.to_datetime(news.Date).dt.date
        unique_ticker = news["Symbol"].unique().tolist()
        news_dict = {name: news.loc[news["Symbol"] == name] for name in unique_ticker}
        values = []
        for ticker in self.tickers:
            dataframe = news_dict[ticker]
            dataframe = dataframe.set_index("Symbol")
            dataframe = dataframe.drop(columns=["Headline"])
            mean = round(dataframe["compound"].mean() * 100, 0)
            values.append(mean)

        company_lst_0 = self.tickers
        company_lst_1 = []
        [company_lst_1.append(company_longName(x)) for x in company_lst_0]

        df = pd.DataFrame(self.tickers, columns=["Symbol"])
        df["company_name"] = company_lst_1
        df["Mean Sentiment"] = values
        df = df.sort_values("Mean Sentiment", ascending=False)
        df["rank"] = range(1, len(df.index) + 1)
        df = df.set_index("rank")

        df = df[df["Mean Sentiment"] >= 1]
        print(df)
        print("good 6")
        return df


if __name__ == "__main__":
    pass
