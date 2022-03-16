from datetime import datetime
from pathlib import Path
import pandas as pd
from finviz.screener import Screener
from os.path import exists
import pickle

from src.data.source_data import Source_Data

# from source_data import Source_Data


class Recommendations0(object):
    def __init__(self, today=str(datetime.now())[:10]):
        self.w1 = "\n* * * * * * * "
        self.w2 = " * * * * * * * \n"
        self.w3 = "[X] [COMPLETE] ~ REC STAGE 0 ~ Compile Screeners to Stock List"
        self.today = today
        self.saveMonth = str(datetime.now())[:7]
        self.saveDay = str(datetime.now())[8:10]
        self.reportDate = str(datetime.now())[:10]

        self.saveRec = Path(f"data/recommenders/{self.saveMonth}/{self.today}/")
        if not self.saveRec.exists():
            self.saveRec.mkdir(parents=True)

        self.saveRaw = Path(f"data/raw/{self.saveMonth}/{self.today}/")
        if not self.saveRaw.exists():
            self.saveRaw.mkdir(parents=True)

        self.saveScreeners = Path(f"data/screeners/{self.saveMonth}/{self.today}/")
        if not self.saveScreeners.exists():
            self.saveScreeners.mkdir(parents=True)

        self.saveTickers = Path(f"data/tickers/{self.saveMonth}/{self.today}/")
        if not self.saveTickers.exists():
            self.saveTickers.mkdir(parents=True)

    def source_data(self):
        stock_list = Screener()
        stock_list.to_csv(f"{str(self.saveTickers)}/finviz_stocks_list.csv")
        s = pd.read_csv(f"{str(self.saveTickers)}/finviz_stocks_list.csv")
        s.to_pickle(f"{str(self.saveTickers)}/finviz_stocks_list.pkl")

        print(f"{self.w1}{self.w2}{self.w3}{self.w1}{self.w2}")
        return

    def clean(self):
        a = list(pd.read_pickle(self.saveTickers / f"finviz_stocks_list.pkl")["Ticker"])
        b = list(set(a))
        c = pd.DataFrame(b, columns=["Symbol"])
        c.to_pickle(self.saveRec / f"recommender_00_return_dataFrame.pkl")
        c.to_pickle(self.saveTickers / f"final_ticker_list.pkl")
        self.w4 = f"[X] [COMPLETE] ~ REC STAGE 0 ~ Clean Stock List [total={len(c)}]"
        print(f"{self.w1}{self.w4}{self.w2}")
        return

    def data_source(self):
        if exists(self.saveRec / f"final_ticker_list.pkl"):
            return
        else:
            self.source_data()
            self.clean()


if __name__ == "__main__":
    today_stamp = str(datetime.now())[:10]
    # Recommendations0(today_stamp).source_data()
    # Recommendations0(today_stamp).clean()
