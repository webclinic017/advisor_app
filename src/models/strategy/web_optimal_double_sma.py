from yahooquery import Ticker
import streamlit as st
import warnings
import pandas as pd
import numpy as np
import yfinance as yf
from itertools import product
import matplotlib.pyplot as plt
import os

warnings.filterwarnings("ignore")
plt.style.use("seaborn")
sm, med, lg = 10, 15, 25
plt.rc("font", size=sm)  # controls default text sizes
plt.rc("axes", labelsize=med)  # fontsize of the x & y labels
plt.rc("axes", titlesize=med)  # fontsize of the axes title
plt.rc("xtick", labelsize=sm)  # fontsize of the tick labels
plt.rc("ytick", labelsize=sm)  # fontsize of the tick labels
plt.rc("legend", fontsize=med)  # legend fontsize
plt.rc("figure", titlesize=lg)  # fontsize of the figure title
plt.rc("axes", linewidth=2)  # linewidth of plot lines
plt.rcParams["legend.fontsize"] = "medium"
legend_properties = {"weight": "bold"}
plt.rcParams["figure.figsize"] = [13, 6.5]
plt.rcParams["figure.dpi"] = 134
plt.rcParams["legend.shadow"] = True
plt.rcParams["legend.borderpad"] = 0.9
plt.rcParams["legend.framealpha"] = 0.1
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["axes.edgecolor"] = "black"
plt.rcParams["legend.loc"] = "upper left"
plt.rcParams["legend.frameon"] = True
plt.rcParams["legend.fancybox"] = True
pd.set_option("display.max_rows", 25)
os.environ["NUMEXPR_MAX_THREADS"] = "24"
os.environ["NUMEXPR_NUM_THREADS"] = "12"


class The_Strategy_2(object):
    def __init__(self, tic):
        self.tic = tic

    def grab_data(self):
        self.raw = yf.download(self.tic, period="1y")

        SMA1 = 2
        SMA2 = 5
        data1 = pd.DataFrame(self.raw["Adj Close"])
        data1.columns = [self.tic]
        data1["SMA1"] = data1[self.tic].rolling(SMA1).mean()
        data1["SMA2"] = data1[self.tic].rolling(SMA2).mean()
        data1["Position"] = np.where(data1["SMA1"] > data1["SMA2"], 1, -1)
        data1["Returns"] = np.log(data1[self.tic] / data1[self.tic].shift(1))
        data1["Strategy"] = data1["Position"].shift(1) * data1["Returns"]
        data1.round(4).tail()
        data1.dropna(inplace=True)
        np.exp(data1[["Returns", "Strategy"]].sum())
        np.exp(data1[["Returns", "Strategy"]].std() * 252 ** 0.5)

        sma1 = range(2, 76, 2)
        sma2 = range(5, 202, 5)
        results = pd.DataFrame()
        for SMA1, SMA2 in product(sma1, sma2):
            data1 = pd.DataFrame(self.raw["Adj Close"])
            data1.columns = [self.tic]
            data1.dropna(inplace=True)
            data1["Returns"] = np.log(data1[self.tic] / data1[self.tic].shift(1))
            data1["SMA1"] = data1[self.tic].rolling(SMA1).mean()
            data1["SMA2"] = data1[self.tic].rolling(SMA2).mean()
            data1.dropna(inplace=True)
            data1["Position"] = np.where(data1["SMA1"] > data1["SMA2"], 1, -1)
            data1["Strategy"] = data1["Position"].shift(1) * data1["Returns"]
            data1.dropna(inplace=True)
            perf = np.exp(data1[["Returns", "Strategy"]].sum())
            results = results.append(
                pd.DataFrame(
                    {
                        "SMA1": SMA1,
                        "SMA2": SMA2,
                        "MARKET(%)": perf["Returns"],
                        "STRATEGY(%)": perf["Strategy"],
                        "OUT": (perf["Strategy"] - perf["Returns"]),
                    },
                    index=[0],
                ),
                ignore_index=True,
            )
        results = results.loc[results["SMA1"] < results["SMA2"]]
        results = (
            results.sort_values("OUT", ascending=False).reset_index(drop=True).head(10)
        )
        S, L, mkt, strat, out = (
            results["SMA1"][0],
            results["SMA2"][0],
            results["MARKET(%)"][0],
            results["STRATEGY(%)"][0],
            results["OUT"][0],
        )
        return S, L, mkt, strat, out


if __name__ == "__main__":

    ticker = "LAZR"

    def get_company_longName(symbol):
        d = Ticker(symbol).quote_type
        return list(d.values())[0]["longName"]

    company_longName = get_company_longName(ticker)

    Short, Long, mkt, strat, out = The_Strategy_2(ticker).grab_data()
    st.write(f"\nBest Short/Long Intervals = {Short} & {Long}\n")
    print(f"\nBest Short/Long Intervals = {Short} & {Long}\n")
