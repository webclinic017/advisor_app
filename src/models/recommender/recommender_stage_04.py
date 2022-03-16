import pandas as pd
import numpy as np
from os.path import exists
from finvizfinance.quote import finvizfinance
from datetime import datetime
from pathlib import Path

from src.tools import functions as f0



class Recommendations4(object):
    def __init__(self, today_stamp):
        self.today_stamp = today_stamp
        self.saveMonth = str(datetime.now())[:7]
        self.saveDay = str(datetime.now())[8:10]

        self.saveRec = Path(f"data/recommenders/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveRec.exists():
            self.saveRec.mkdir(parents=True)


    def create_final(self):
        if exists(self.saveRec / "recommender_04_return_dataFrame.pkl"):
            return
        else:
            df_total_01 = pd.read_pickle(self.saveRec / "recommender_01_return_dataFrame.pkl")
            df_total_02 = pd.read_pickle(self.saveRec / "recommender_02_return_dataFrame.pkl")  
            df_total_03 = pd.read_pickle(self.saveRec / "recommender_03_return_dataFrame.pkl")  

            df_total_01 = df_total_01[["Symbol", "Score"]]
            df_total_01_2 = df_total_01[df_total_01["Symbol"].isin(list(df_total_03["Symbol"]))]
            df_total_01_2 = df_total_01_2.sort_values("Symbol")
            df_total_02 = df_total_02[
                [
                    "Symbol",
                    "RS_Rating",
                    "Returns_multiple",
                    "currentClose",
                    "20 Day MA",
                    "50 Day Ma",
                    "200 Day MA",
                    "52 Week Low",
                    "52 week High",
                ]
            ]
            df_total_02.columns = [
                "Symbol",
                "RS_Rating",
                "Returns_Multiple",
                "Current_Price",
                "20_Day_MA",
                "50_Day_Ma",
                "200_Day_MA",
                "52_Week_Low",
                "52_week_High",
            ]
            df_total_02[
                ["Current_Price", "52_Week_Low", "52_week_High"]
                ] = df_total_02[["Current_Price", "52_Week_Low", "52_week_High"]
                ].applymap("${0:.2f}".format)
            df_total_02_2 = df_total_02[df_total_02["Symbol"].isin(list(df_total_03["Symbol"]))]
            df_total_02_2 = df_total_02_2.sort_values("Symbol")
            df_total_02_2 = df_total_02_2.reset_index()
            df_total_02_2 = df_total_02_2[
                [
                    "Symbol",
                    "RS_Rating",
                    "Returns_Multiple",
                    "Current_Price",
                    "20_Day_MA",
                    "50_Day_Ma",
                    "200_Day_MA",
                    "52_Week_Low",
                    "52_week_High",
                ]
            ]

            df_total_03 = df_total_03.sort_values("Symbol")
            target_d3 = []

            for stock in list(df_total_03["Symbol"]):
                try:
                    target_d3.append(float(finvizfinance(stock).TickerFundament()["Target Price"]))
                except Exception:
                    target_d3.append(0.0)

            current = []
            for stock in list(df_total_03["Symbol"]):
                current.append(float(finvizfinance(stock).TickerFundament()["Price"]))

            df_report = pd.DataFrame(list(df_total_03["Symbol"]), columns=["Symbol"])

            company_lst = []
            for i in df_report["Symbol"]:
                company_lst.append(f0.company_longName(i))
            df_report["Company"] = company_lst
            df_report["Sentiment_Score"] = df_total_03["Mean Sentiment"].values
            df_report["Analyst_Score"] = df_total_01_2["Score"].values
            df_report["Relative_Strength"] = df_total_02_2["RS_Rating"].values
            df_report["Returns_Multiple"] = df_total_02_2["Returns_Multiple"].values
            df_report["Current_Price"] = current
            df_report["1yr_Target"] = target_d3
            df_report["Est_G/L"] = round(
                (
                    (df_report["1yr_Target"] - df_report["Current_Price"])
                    / df_report["Current_Price"]
                )
                * 100,
                2,
            )
            df_report["52_Week_Low"] = df_total_02_2["52_Week_Low"].values
            df_report["52_week_High"] = df_total_02_2["52_week_High"].values
            df_report["20_Day_MA"] = df_total_02_2["20_Day_MA"].values
            df_report["50_Day_Ma"] = df_total_02_2["50_Day_Ma"].values
            df_report["200_Day_MA"] = df_total_02_2["200_Day_MA"].values
            df_report = df_report.sort_values("Est_G/L", ascending=False)
            df_report["rank"] = range(1, len(df_report["Symbol"]) + 1)
            df_report = pd.DataFrame(df_report).set_index("rank")

            new_df = pd.DataFrame(df_report)
            new_df = new_df[new_df["Est_G/L"] > 0.01]

            analyst_recom = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
            adj_analyst_recom = list(np.arange(50.0, 101.0, 3.125))
            d1=dict(zip(analyst_recom, adj_analyst_recom))
            adj__analyst_lst = []

            for i in new_df['Analyst_Score']:
                for key, val in d1.items():
                    if i == key:
                        adj__analyst_lst.append(round(val,2))            
            new_df['adj_analyst_recom'] = new_df
            new_df["my_score"] = ((new_df["Sentiment_Score"])+ (new_df["adj_analyst_recom"])+ (new_df["Relative_Strength"])) / 3
            
            new_df = pd.DataFrame(new_df).sort_values("my_score", ascending=False)
            new_df["rank"] = range(1, len(new_df["Symbol"]) + 1)
            abc = pd.DataFrame(new_df).set_index(["rank", "my_score"])
            abc.to_pickle(self.saveRec / "recommender_04_return_dataFrame.pkl")
            return