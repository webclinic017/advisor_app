import warnings
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib
import streamlit as st
from matplotlib import pyplot as plt
from sklearn.mixture import GaussianMixture
import os

import src.tools.functions as f0

warnings.filterwarnings("ignore")
matplotlib.use("Agg")
plt.style.use(["seaborn-darkgrid", "seaborn-deep", "seaborn-poster", "seaborn-whitegrid"])
plt.rcParams["figure.figsize"] = [10, 7]
plt.rcParams["figure.dpi"] = 100
plt.rcParams["figure.autolayout"] = True
plt.rcParams["lines.linewidth"] = 3
plt.rcParams["axes.grid"] = True
os.environ["NUMEXPR_MAX_THREADS"] = "24"
os.environ["NUMEXPR_NUM_THREADS"] = "12"



class The_Financial_Signal_Processing(object):
    
    
    def __init__(self, ticker):
        self.ticker = ticker
        yf_prices = yf.download(self.ticker, start="2015-01-01")
        company_longName = f0.company_longName(self.ticker)

        x = f"{company_longName} [{self.ticker}]"
        st.subheader(f"𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄙 Financial Signaling · {x} 𝄙𝄙𝄙𝄘𝄘𝄗𝄗𝄖𝄖")


        # 1 - STATIONARY:
        prices = yf_prices["Adj Close"]
        fig, ax = plt.subplots(1, 2)
        prices.plot(title=f"{str(self.ticker).upper()} Price", ax=ax[0], grid=True, linewidth=2)
        prices.plot.hist(
            title=f"{str(self.ticker).upper()} Price Distribution",
            ax=ax[1],
            grid=True,
            bins=30,
            )
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)


        # 2 - LOG RETURNS:
        rs = prices.apply(np.log).diff(1)
        fig, ax = plt.subplots(1, 2)
        rs.plot(title=f"{str(self.ticker).upper()} Returns", ax=ax[0], grid=True, linewidth=2)
        rs.plot.hist(title=f"{str(self.ticker).upper()} Returns Distribution", ax=ax[1], grid=True, bins=30)
        plt.tight_layout()
        plt.title(f"{str(self.ticker).upper()} Log Returns Distribution")
        st.pyplot(fig)
        plt.close(fig)


        # 3 - ROLLING STATISTICS:
        w = 22
        s1 = rs.rolling(w).mean()
        s2 = rs.rolling(w).std()
        s3 = rs.rolling(w).skew()
        s4 = rs.rolling(w).kurt()
        signals = pd.concat([s1, s2, s3, s4], axis=1)
        signals.columns = ["mean", "std dev", "skew", "kurtosis"]

        # fig, ax = plt.subplots()
        # signals.plot(subplots=True)
        # plt.legend(signals.columns)
        # plt.tight_layout()
        # st.pyplot(fig)
        # plt.close(fig)


        # 4 - Volatility Regimes (Gaussian Mixture)
        prices = yf_prices["Adj Close"]
        rs = prices.apply(np.log).diff(1)
        w = 22
        vol = rs.rolling(w).std()
        vol = vol.dropna()
        labels = GaussianMixture(2).fit_predict(vol.values.reshape(-1, 1))
        prices = prices.reindex(vol.index)

        fig, ax = plt.subplots(nrows=1, ncols=1)
        prices[labels == 0].plot(style="bo", alpha=0.2, label="low")
        prices[labels == 1].plot(style="ro", alpha=0.2, label="high")
        plt.title(f"{str(self.ticker).upper()} Volatility Regimes (Gaussian Mixture)")
        plt.tight_layout()
        plt.legend()
        st.pyplot(fig)
        plt.close(fig)
