import numpy as np
import pandas as pd

import matplotlib
import matplotlib as mpl
from yahoo_fin.stock_info import tickers_dow

matplotlib.use("Agg")
from matplotlib import style
from matplotlib import pyplot as plt

plt.style.use("ggplot")
sm, med, lg = 10, 15, 20
plt.rc("font", size=sm)  # controls default text sizes
plt.rc("axes", titlesize=med)  # fontsize of the axes title
plt.rc("axes", labelsize=med)  # fontsize of the x & y labels
plt.rc("xtick", labelsize=sm)  # fontsize of the tick labels
plt.rc("ytick", labelsize=sm)  # fontsize of the tick labels
plt.rc("legend", fontsize=sm)  # legend fontsize
plt.rc("figure", titlesize=lg)  # fontsize of the figure title
plt.rc("axes", linewidth=2)  # linewidth of plot lines
plt.rcParams["figure.figsize"] = [18, 10]
plt.rcParams["figure.dpi"] = 150

import yfinance as yf
import bs4 as bs
import requests
import pickle
from pandas.io.pickle import read_pickle
from sklearn.decomposition import PCA

plt.style.use("ggplot")
from pathlib import Path

path = Path.cwd()
import streamlit as st


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


class The_PCA_Analysis(object):


    def __init__(self, tickers, lst_name):
        self.tickers = tickers
        self.lst_name = lst_name
        self.prices = yf.download(self.tickers, period="1y")["Adj Close"]
        self.rs = self.prices.apply(np.log).diff(1)


    def build_pca(self):

        fig, ax = plt.subplots()
        ax = self.rs.plot(
            legend=0,
            figsize=(10, 6),
            grid=True,
            title=f"Daily Returns of the Stocks In The ({self.lst_name} ticker list)",
        )
        plt.tight_layout()
        st.pyplot()
        #plt.close()


        fig, ax = plt.subplots()
        (self.rs.cumsum().apply(np.exp)).plot(
            legend=0,
            figsize=(10, 6),
            grid=True,
            title=f"Cumulative Returns of the Stocks In The ({self.lst_name} ticker list)",
        )
        plt.tight_layout()
        st.pyplot()
        #plt.close()


        pca = PCA(1).fit(self.rs.fillna(0))
        pc1 = pd.Series(index=self.rs.columns, data=pca.components_[0])

        fig, ax = plt.subplots()
        pc1.plot(
            figsize=(10, 6),
            xticks=[],
            grid=True,
            title=f"First Principal Component In The ({self.lst_name} ticker list)",
        )
        plt.tight_layout()
        st.pyplot()
        #plt.close()


        fig, ax = plt.subplots()
        weights = abs(pc1) / sum(abs(pc1))
        myrs = (weights * self.rs).sum(1)
        myrs.cumsum().apply(np.exp).plot(
            figsize=(10, 6),
            grid=True,
            title=f"Cumulative Daily Returns of 1st Principal Component Stock In The ({self.lst_name} ticker list)",
        )
        st.pyplot()
        #plt.close()


        prices = yf.download(["^GSPC"], start="2020-01-01")["Adj Close"]
        rs_df = pd.concat([myrs, prices.apply(np.log).diff(1)], 1)
        rs_df.columns = ["PCA Portfolio", "SP500_Index"]
        fig, ax = plt.subplots()
        rs_df.dropna().cumsum().apply(np.exp).plot(
            subplots=True, figsize=(10, 6), grid=True, linewidth=3
        )
        plt.tight_layout()
        st.pyplot()
        #plt.close()


        fig, ax = plt.subplots(2, 1, figsize=(10, 6))
        pc1.nlargest(10).plot.bar(
            ax=ax[0],
            color="blue",
            grid=True,
            title="Stocks with Highest PCA Score -OR- Least Negative PCA Weights",
        )
        pc1.nsmallest(10).plot.bar(
            ax=ax[1],
            color="green",
            grid=True,
            title="Stocks with Lowest PCA Score -OR- Most Negative PCA Weights",
        )
        plt.tight_layout()
        st.pyplot()
        #plt.close()


        ws = [-1,] * 10 + [
            1,
        ] * 10
        myrs = self.rs[pc1.nlargest(10).index].mean(1)

        fig, ax = plt.subplots()
        myrs.cumsum().apply(np.exp).plot(
            figsize=(15, 5),
            grid=True,
            linewidth=3,
            title=f"PCA Portfolio (10 Most Impactful) vs The ({self.lst_name} ticker list)",
        )
        prices["2020":].apply(np.log).diff(1).cumsum().apply(np.exp).plot(
            figsize=(10, 6), grid=True, linewidth=3
        )
        plt.legend(["PCA Selection", "SP500_Index"])
        plt.tight_layout()
        st.pyplot()
        #plt.close()


        fig, ax = plt.subplots()
        ws = [-1,] * 10 + [1,] * 10
        myrs = self.rs[pc1.nsmallest(10).index].mean(1)
        myrs.cumsum().apply(np.exp).plot(
            figsize=(15, 5),
            grid=True,
            linewidth=3,
            title=f"PCA Portfolio (10 Least Impactful) vs The ({self.lst_name} ticker list)",
        )
        prices["2020":].apply(np.log).diff(1).cumsum().apply(np.exp).plot(
            figsize=(10, 6), grid=True, linewidth=3
        )
        plt.legend(["PCA Selection", "SP500_Index"])
        plt.tight_layout()
        st.pyplot()
        #plt.close()


        if len(self.tickers) > 20:
            ws = [-1,] * 10 + [1,] * 10
            myrs = (self.rs[list(pc1.nsmallest(10).index) + list(pc1.nlargest(10).index)]* ws).mean(1)

            fig, ax = plt.subplots()
            myrs.cumsum().apply(np.exp).plot(
                figsize=(15, 5),
                grid=True,
                linewidth=3,
                title=f"PCA Portfolio (10 Most & Least Impactful) vs The ({self.lst_name} Ticker List)",
            )
            prices["2020":].apply(np.log).diff(1).cumsum().apply(np.exp).plot(
                figsize=(10, 6), grid=True, linewidth=3
            )
            plt.legend(["PCA Selection", "SP500_Index"])
            plt.tight_layout()
            st.pyplot()
            #plt.close()


            st.title(f"Below Are The Principal Components From The Ticker List:")
            st.header("Copy These Lists and Save Them To Use In the Other 2 Portfolio Models")
            st.subheader("LARGEST PCA VALUES:")

            for i in pc1.nlargest(10).index:
                st.write(i)
            st.subheader("SMALLEST PCA VALUES:")
            for i in pc1.nsmallest(10).index:
                st.write(i)

        else:
            return


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


if __name__ == "__main__":
    import yahoo_fin.stock_info as si
    
    The_PCA_Analysis(tickers_dow(), "dow")


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


