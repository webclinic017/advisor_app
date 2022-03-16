#  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *     *
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

import warnings

warnings.filterwarnings("ignore")
from datetime import datetime, date, timedelta
from pathlib import Path

today = str(datetime.now())[:10]
import matplotlib
import matplotlib as mpl

matplotlib.use("Agg")
from matplotlib import style
from matplotlib import pyplot as plt

plt.style.use("seaborn-poster")
sm, med, lg = 10, 15, 20
plt.rc("font", size=sm)  # controls default text sizes
plt.rc("axes", titlesize=med)  # fontsize of the axes title
plt.rc("axes", labelsize=med)  # fontsize of the x & y labels
plt.rc("xtick", labelsize=sm)  # fontsize of the tick labels
plt.rc("ytick", labelsize=sm)  # fontsize of the tick labels
plt.rc("legend", fontsize=sm)  # legend fontsize
plt.rc("figure", titlesize=lg)  # fontsize of the figure title
plt.rc("axes", linewidth=2)  # linewidth of plot lines
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import itertools
import streamlit as st
import yfinance as yf
from datetime import datetime
import backtrader as bt


from datetime import datetime
import backtrader as bt

# Create a Stratey
class SmaStrategy(bt.Strategy):
    params = (("ma_period", 20),)

    def __init__(self):
        # keep track of close price in the series
        self.data_close = self.datas[0].close

        # keep track of pending orders
        self.order = None

        # add a simple moving average indicator
        self.sma = bt.ind.SMA(self.datas[0], period=self.params.ma_period)

    def log(self, txt):
        """Logging function"""
        dt = self.datas[0].datetime.date(0).isoformat()
        # st.text(f'{dt}, {txt}')
        print((f"{dt}, {txt}"))

    def notify_order(self, order):
        # set no pending order
        self.order = None

    def next(self):
        # do nothing if an order is pending
        if self.order:
            return

        # check if there is already a position
        if not self.position:
            # buy condition
            if self.data_close[0] > self.sma[0]:
                self.order = self.buy()
        else:
            # sell condition
            if self.data_close[0] < self.sma[0]:
                self.order = self.sell()

    def stop(self):
        self.log(
            f"(ma_period = {self.params.ma_period:2d}) --- Terminal Value: {self.broker.getvalue():.2f}"
        )


def bt_sma_strategy_optimization_run(tick):
    # download data
    data = bt.feeds.YahooFinanceData(
        dataname=tick, fromdate=datetime(2021, 1, 3), todate=datetime(2021, 9, 15)
    )
    # create a Cerebro entity
    cerebro = bt.Cerebro(stdstats=False)
    # set up the backtest
    cerebro.adddata(data)
    cerebro.optstrategy(SmaStrategy, ma_period=range(2, 69))
    cerebro.broker.setcash(1000.0)
    cerebro.run(maxcpus=4)


bt_sma_strategy_optimization_run(
    "/home/gordon/modern_millennial_market_mapping/src/models/backtest/z_test_env/AAPL.pkl"
)
