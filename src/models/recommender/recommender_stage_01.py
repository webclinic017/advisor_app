from finvizfinance.quote import finvizfinance
import pandas as pd
from pathlib import Path
from datetime import datetime
from os.path import exists


class Recommendations1(object):
    def __init__(self, today):
        self.today = today
        self.saveMonth = str(today)[:7]
        self.saveDay = str(today)[8:10]
        self.reportDate = str(today)[:10]

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


    def run_rec1(self):
        if exists(self.saveRec / f"recommender_01_return_dataFrame.pkl"):
            return
        elif exists(self.saveRec / f"recommender_00_return_dataFrame.pkl"):
            self.ticker_list = list(
                pd.read_pickle(self.saveRec / f"recommender_00_return_dataFrame.pkl")[
                    "Symbol"
                ]
            )
        else:
            print(
                f"* * * [ ERROR ] No File {str(str(self.saveRec) + 'recommender_00_return_dataFrame.pkl')} * * *"
            )

        self.recommendations = []

        for s in self.ticker_list:
            try:
                recommendation = finvizfinance(s).TickerFundament()["Recom"]
            except Exception:
                recommendation = 6.0

            if recommendation == "-":
                recommendation = 6.0

            self.recommendations.append(round(float(recommendation), 2))

        dataframe = pd.DataFrame(
            list(zip(self.ticker_list, self.recommendations)),
            columns=["Company", "Recommendations"],
        ).sort_values("Recommendations")
        dataframe.to_pickle(self.saveRec / "recommender_01A_return_dataFrame.pkl")
        dataframe_02 = dataframe[dataframe["Recommendations"] < 2.6]
        dataframe_02.columns = ["Symbol", "Score"]
        dataframe_02["rank"] = range(1, len(dataframe_02["Symbol"]) + 1)
        dataframe_02 = dataframe_02.set_index("rank")
        dataframe_02.to_pickle(self.saveRec / "recommender_01_return_dataFrame.pkl")
        return

    def run_rec1_personal_port(self, personal_port):
        self.ticker_list = personal_port
        self.recommendations = []

        for s in self.ticker_list:
            try:
                recommendation = finvizfinance(s).TickerFundament()["Recom"]
            except Exception:
                recommendation = 6.0

            if recommendation == "-":
                recommendation = 6.0

            self.recommendations.append(round(float(recommendation), 2))

        dataframe = pd.DataFrame(
            list(zip(self.ticker_list, self.recommendations)),
            columns=["Company", "Recommendations"],
        ).sort_values("Recommendations")
        dataframe_02 = dataframe[dataframe["Recommendations"] < 2.6]
        dataframe_02.columns = ["Symbol", "Score"]
        dataframe_02["rank"] = range(1, len(dataframe_02["Symbol"]) + 1)
        dataframe_02 = dataframe_02.set_index("rank")
        return dataframe, dataframe_02


if __name__ == "__main__":
    Recommendations1()
