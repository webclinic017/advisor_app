import yfinance as yf
from yahooquery import Ticker
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
from tabulate import tabulate
import warnings
import streamlit as st
from datetime import datetime

warnings.filterwarnings("ignore")
mpl.use("Agg")
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


def MovingAverageCrossStrategy(
    stock_symbol,
    start_date="2018-01-01",
    end_date=datetime.now(),
    short_window=20,
    long_window=50,
    moving_avg="SMA",
    display_table=True,
):
    """
    The function takes the stock symbol, time-duration of analysis,
    look-back periods and the moving-average type(SMA or EMA) as input
    and returns the respective MA Crossover chart along with the buy/sell signals for the given period.
    """
    # stock_symbol - (str)stock ticker as on Yahoo finance. Eg: 'ULTRACEMCO.NS'
    # start_date - (str)start analysis from this date (format: 'YYYY-MM-DD') Eg: '2018-01-01'
    # end_date - (str)end analysis on this date (format: 'YYYY-MM-DD') Eg: '2020-01-01'
    # short_window - (int)lookback period for short-term moving average. Eg: 5, 10, 20
    # long_window - (int)lookback period for long-term moving average. Eg: 50, 100, 200
    # moving_avg - (str)the type of moving average to use ('SMA' or 'EMA')
    # display_table - (bool)whether to display the date and price table at buy/sell positions(True/False)

    # import the closing price data of the stock for the aforementioned period of time in Pandas dataframe
    start1 = datetime(*map(int, start_date.split("-")))
    end1 = datetime(*map(int, end_date.split("-")))

    # stock_df = web.DataReader(stock_symbol, 'yahoo', start = start, end = end)['Close']
    stock_df = yf.download(stock_symbol, period="max", parse_dates=True)["Close"]
    # stock_df = yf.download(stock_symbol, start=start1, end=end1, parse_dates=True)[
    #     "Close"
    # ]

    stock_df = pd.DataFrame(stock_df)  # convert Series object to dataframe
    stock_df.columns = {"Close Price"}  # assign new colun name
    stock_df.dropna(axis=0, inplace=True)  # remove any null rows

    # column names for long and short moving average columns
    short_window_col = str(short_window) + "_" + moving_avg
    long_window_col = str(long_window) + "_" + moving_avg

    if moving_avg == "SMA":
        # Create a short simple moving average column
        stock_df[short_window_col] = (
            stock_df["Close Price"].rolling(window=short_window, min_periods=1).mean()
        )
        # Create a long simple moving average column
        stock_df[long_window_col] = (
            stock_df["Close Price"].rolling(window=long_window, min_periods=1).mean()
        )

    elif moving_avg == "EMA":
        # Create short exponential moving average column
        stock_df[short_window_col] = (
            stock_df["Close Price"].ewm(span=short_window, adjust=False).mean()
        )
        # Create a long exponential moving average column
        stock_df[long_window_col] = (
            stock_df["Close Price"].ewm(span=long_window, adjust=False).mean()
        )

    # create a new column 'Signal' such that if faster moving average is greater than slower moving average
    # then set Signal as 1 else 0.
    stock_df["Signal"] = 0.0
    stock_df["Signal"] = np.where(
        stock_df[short_window_col] > stock_df[long_window_col], 1.0, 0.0
    )

    # create a new column 'Position' which is a day-to-day difference of the 'Signal' column.
    stock_df["Position"] = stock_df["Signal"].diff()

    # plot close price, short-term and long-term moving averages
    fig, ax = plt.subplots()
    plt.tick_params(axis="both", labelsize=15)
    stock_df.loc["2020":, "Close Price"].plot(color="k", lw=1, label="Close Price")
    stock_df.loc["2020":][short_window_col].plot(
        color="b", lw=1, label=short_window_col
    )
    stock_df.loc["2020":][long_window_col].plot(color="g", lw=1, label=long_window_col)
    # plot 'buy' signals
    plt.plot(
        stock_df.loc["2020":][stock_df["Position"] == 1].index,
        stock_df.loc["2020":][short_window_col][stock_df["Position"] == 1],
        "^",
        markersize=15,
        color="g",
        alpha=0.7,
        label="buy",
    )
    # plot 'sell' signals
    plt.plot(
        stock_df.loc["2020":][stock_df["Position"] == -1].index,
        stock_df.loc["2020":][short_window_col][stock_df["Position"] == -1],
        "v",
        markersize=15,
        color="r",
        alpha=0.7,
        label="sell",
    )
    plt.ylabel("Price in $", fontsize=20, fontweight="bold")
    plt.xlabel("Date", fontsize=20, fontweight="bold")
    plt.title(
        f"{stock_symbol} - {str(moving_avg)} Crossover",
        fontsize=30,
        fontweight="bold",
    )
    plt.grid(True, color="k", linestyle="-", linewidth=1, alpha=0.3)
    ax.legend(loc="best", prop={"size": 16})
    plt.tight_layout()
    plt.show()
    st.pyplot(fig)

    if display_table is True:
        df_pos = stock_df[(stock_df["Position"] == 1) | (stock_df["Position"] == -1)]
        df_pos["Position"] = df_pos["Position"].apply(
            lambda x: "Buy" if x == 1 else "Sell"
        )
        st.text(tabulate(df_pos.loc["2020":], headers="keys", tablefmt="psql"))


# if __name__ == "__main__":

#     stock_ticker = "MATIC-USD"

#     def get_company_longName(symbol):
#         d = Ticker(symbol).quote_type
#         return list(d.values())[0]["longName"]

#     company_longName = get_company_longName(stock_ticker)

#     MovingAverageCrossStrategy(
#         stock_symbol=stock_ticker,
#         longName=company_longName,
#         start_date="2019-01-01",
#         end_date=datetime.now(),
#         short_window=20,
#         long_window=50,
#         moving_avg="SMA",
#         display_table=True,
#     )

#     MovingAverageCrossStrategy(
#         stock_symbol=stock_ticker,
#         longName=company_longName,
#         start_date="2019-01-01",
#         end_date=datetime.now(),
#         short_window=20,
#         long_window=50,
#         moving_avg="EMA",
#         display_table=True,
#     )
