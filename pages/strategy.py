from re import S
import streamlit as st
from datetime import datetime, date
from pathlib import Path
import time
from yahooquery import Ticker
import pandas as pd
import matplotlib.pyplot as plt

import src.models.strategy as s1
from src.tools import functions as f0
from src.tools import lists as l0

plt.style.use("ggplot")
sm, med, lg = "20", "25", "30"
plt.rcParams["font.size"] = sm  # controls default text sizes
plt.rc("axes", titlesize=med)  # fontsize of the axes title
plt.rc("axes", labelsize=med)  # fontsize of the x & y labels
plt.rc("xtick", labelsize=sm)  # fontsize of the tick labels
plt.rc("ytick", labelsize=sm)  # fontsize of the tick labels
plt.rc("legend", fontsize=sm)  # legend fontsize
plt.rc("figure", titlesize=lg)  # fontsize of the figure title
plt.rc("axes", linewidth=2)  # linewidth of plot lines
plt.rcParams["figure.figsize"] = [15, 13]
plt.rcParams["figure.dpi"] = 113
plt.rcParams["axes.facecolor"] = "silver"


class Strategy(object):

    def __init__(self, today_stamp):
        self.today_stamp = str(today_stamp)[:10]
        self.saveMonth = str(datetime.now())[:7]
        self.saveDay = str(datetime.now())[8:10]
        self.saveRec = Path(f"data/recommenders/{str(today_stamp)[:4]}/{self.saveMonth}/{self.today_stamp}/")


    def run_the_strats(self):
        st.sidebar.header("[3] Select Stock")
        select_stocks = st.sidebar.radio(
            "Pick Stocks", 
            (
                "Single Stock", 
                "Recommended Stocks", 
                "Personal Portfolio"
            )
        )
        
        
        if select_stocks == "Single Stock":
            self.stock_ticker = st.sidebar.text_input(
                label="Enter Stock In ALL CAPS [example: TSLA]", 
                value="TSLA"
            )        

            st.sidebar.write(" *" * 25)
            st.sidebar.header("[4] Select Method [All or 1]")
            method_strat = st.sidebar.radio(
                "Pick Method", 
                (
                    "Individual Strategy", 
                    "Run All Strategies"
                )
            )
            
            
            if method_strat == "Run All Strategies":
                st.sidebar.write(" *" * 25)            
                if st.sidebar.button("Run Strategies"):
                    hammerTime = Ticker(
                        self.stock_ticker,
                        asynchronous=False,
                        formatted=False,
                        backoff_factor=0.34,
                        progress=True,
                        validate=True,
                        verify=True,
                    )
                    hammer_hist = hammerTime.history(period='2y').reset_index().set_index('date')
                    hammer_hist.index = pd.to_datetime(hammer_hist.index)
                    data = hammer_hist.rename(columns={'symbol': 'ticker'})
                    try:
                        del data['ticker']
                        del data['splits']
                        del data['dividends']
                    except Exception:
                        pass            

                    self.run_movAvg_sma_ema(self.stock_ticker, data, "SMA")
                    self.run_optimal_sma(self.stock_ticker, data)
                    self.run_overBought_overSold(self.stock_ticker, data)
                    self.run_supportResistance(self.stock_ticker)
                    self.run_strategyII(self.stock_ticker)


            if method_strat == "Individual Strategy":
                st.sidebar.write(" *" * 25)
                
                st.sidebar.header("[5] Select Model")
                model = st.sidebar.radio("Choose A Model", l0.feature_strategy, index=0)
                st.sidebar.write(" *" * 25)

                if model == "-Select-Model-":
                    self.run_homePage()
                    
                else:
                    if st.sidebar.button("Run Strategy"):
                        hammerTime = Ticker(
                            self.stock_ticker,
                            asynchronous=False,
                            formatted=False,
                            backoff_factor=0.34,
                            progress=True,
                            validate=True,
                            verify=True,
                        )
                        hammer_hist = hammerTime.history(period='2y').reset_index().set_index('date')
                        hammer_hist.index = pd.to_datetime(hammer_hist.index)
                        data = hammer_hist.rename(columns={'symbol': 'ticker'})
                        try:
                            del data['ticker']
                            del data['splits']
                            del data['dividends']
                        except Exception:
                            pass                        

                        if model == "Moving-Average - SMA & EMA":
                            st.sidebar.write("__" * 25)
                            self.run_movAvg_sma_ema(self.stock_ticker, data, sma_ema_opt='SMA', p_out=True, inter='1d')

                        if model == "Optimal SMA":
                            self.run_optimal_sma(self.stock_ticker, data)

                        if model == "OverBought & OverSold":
                            self.run_overBought_overSold(self.stock_ticker, data)

                        if model == "Support & Resistance Lines":
                            self.run_supportResistance(self.stock_ticker)

                        if model == "Strategy II":
                            self.run_strategyII(self.stock_ticker)
                            
                        if model == "Indicators":
                            s1.ii().kingpin(self.stock_ticker)



        if select_stocks == "Recommended Stocks":

            report_date = st.sidebar.date_input(
            label="> recommender date:",
                value=date(2021, 7, 14),
                min_value=date(2021, 7, 14),
                max_value=date.today(),
                key="date to run proof",
                help="Select a date in the range between 2021.07.15 - 2021.08.26. \
                    This date will be the date the recommender model was run and we \
                        will use the resulting tickers for our proof",
            )
            name_lst = st.sidebar.radio(
                label="", 
                options=(
                    'minimum_volatility_portfolio',    
                    'maximum_sharpe_ratio',
                    'maximum_sharpe_equalWT',
                    'monte_carlo_cholesky',
                ),
                index=1
            )
            stock_ticker = f0.recommended_stocks_2(name_lst, report_date)            


            if method_strat == "Run All Strategies":
                if st.sidebar.button("Run Strategies"):
                    for i in stock_ticker:
                        self.run_movAvg_sma_ema(i, "SMA")
                        self.run_optimal_sma(i)
                        self.run_overBought_overSold(i)
                        self.run_supportResistance(i)
                        # self.run_strategyII(i)
           

            if method_strat == "Individual Strategy":
                st.sidebar.header("[5] Select Model")
                model = st.sidebar.radio("Choose A Model", l0.feature_strategy)
                st.sidebar.write(" *" * 25)

                if model == "-Select-Model-":
                    self.run_homePage()

                if model == "Moving-Average - SMA & EMA":
                    sma_ema_choice = st.sidebar.radio("Choose Moving Average Method", ("SMA", "EMA"))
                    inter = st.sidebar.radio('Interval',
                        ('1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo'),
                        index=8
                    )                    
                    st.sidebar.write("__" * 25)
                    if st.sidebar.button("Run Strategy"):
                        hammerTime = Ticker(
                            stock_ticker,
                            asynchronous=True,
                            formatted=False,
                            backoff_factor=0.34,
                            progress=True,
                            validate=True,
                            verify=True,
                        )
                        hammer_hist = hammerTime.history(period='2y').reset_index().set_index('date')
                        hammer_hist.index = pd.to_datetime(hammer_hist.index)
                        hammer_hist = hammer_hist.rename(columns={'symbol': 'ticker'})                    
                        for i in stock_ticker:
                            data = pd.DataFrame(hammer_hist[hammer_hist['ticker'] == i])
                            self.run_movAvg_sma_ema(i, data, sma_ema_choice, True, inter)


                if model == "Optimal SMA":
                    if st.sidebar.button("Run Strategy"):
                        hammerTime = Ticker(
                            stock_ticker,
                            asynchronous=True,
                            formatted=False,
                            backoff_factor=0.34,
                            progress=True,
                            validate=True,
                            verify=True,
                        )
                        hammer_hist = hammerTime.history(period='2y').reset_index().set_index('date')
                        hammer_hist.index = pd.to_datetime(hammer_hist.index)
                        hammer_hist = hammer_hist.rename(columns={'symbol': 'ticker'})                            
                        for i in stock_ticker:
                            data = pd.DataFrame(hammer_hist[hammer_hist['ticker'] == i])
                            self.run_optimal_sma(i, data)


                if model == "OverBought & OverSold":
                    if st.sidebar.button("Run Strategy"):
                        for i in stock_ticker:
                            self.run_overBought_overSold(i)


                if model == "Support & Resistance Lines":
                    if st.sidebar.button("Run Strategy"):
                        for i in stock_ticker:
                            self.run_supportResistance(i)


                if model == "Strategy II":
                    if st.sidebar.button("Run Strategy"):
                        for i in stock_ticker:
                            self.run_strategyII(i)


        if select_stocks == "Personal Portfolio":
            st.sidebar.write(" *" * 25)
            stock_ticker = st.sidebar.text_input(
                label="Enter Your Own Stock List To Model The various Machine Learning & Algo Trading Strategies",
                value="TSLA NVDA AAPL ASML SNOW",
            )
            stock_ticker = stock_ticker.split()
            st.sidebar.write(" *" * 25)

            if method_strat == "Run All Strategies":
                if st.sidebar.button("Run Strategies", key='a'):
                    for s in stock_ticker:
                        self.run_movAvg_sma_ema(s, "SMA")
                        self.run_optimal_sma(s)
                        self.run_overBought_overSold(s)
                        self.run_supportResistance(s)
                        self.run_strategyII(s)


            if method_strat == "Individual Strategy":
                st.sidebar.header("[5] Select Model")
                model = st.sidebar.radio("Choose A Model", l0.feature_strategy)
                st.sidebar.write(" *" * 25)               

                if model == "Moving-Average - SMA & EMA":
                    sma_ema_choice = st.sidebar.radio("Choose Moving Average Method", ("SMA", "EMA"))
                    inter = st.sidebar.radio('Interval',
                        ('1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo'),
                        index=8
                    )
                    st.sidebar.write("__" * 25)
                    if st.sidebar.button("Run Strategies", key='b'):
                        hammerTime = Ticker(
                            stock_ticker,
                            asynchronous=True,
                            formatted=False,
                            backoff_factor=0.34,
                            progress=True,
                            validate=True,
                            verify=True,
                        )
                        hammer_hist = hammerTime.history(period='2y').reset_index().set_index('date')
                        hammer_hist.index = pd.to_datetime(hammer_hist.index)
                        data = hammer_hist.rename(columns={'symbol': 'ticker'})
                                
                        del data['ticker']
                        del data['dividends']
                        st.dataframe(data)                     
                                                
                        for s in stock_ticker:
                            self.run_movAvg_sma_ema(s, data, sma_ema_choice, True, inter)

                else:
                    if st.sidebar.button("Run Strategies", key='c'):

                        if model == "Optimal SMA":
                            for s in stock_ticker:
                                self.run_optimal_sma(s)


                        if model == "OverBought & OverSold":
                            for s in stock_ticker:
                                self.run_overBought_overSold(s)


                        if model == "Support & Resistance Lines":
                            for s in stock_ticker:
                                self.run_supportResistance(s)


                        if model == "Strategy II":
                            for s in stock_ticker:
                                self.run_strategyII(s)


    def run_homePage(self):
        st.header("[Strategy Home Page]")
        st.write(" *" * 25)

        st.subheader(" > General Analysis Components ")
        with st.expander("Expand For Details", expanded=False):
            st.subheader("Moving Averages")
            st.write(
                """
                * Double Moving Averages
                * Exponential Moving Average (EMA)
                * Simple Moving Average (SMA)
                * Bollinger Bands
                * MOM
                * MACD
                * RSI
                * APO
                """
            )
            st.subheader("Regression")
            st.write(
                """
                * Linear Regression
                * Quadratic Regression 2 & 3
                * KNN
                * Lasso
                * Ridge
                * Logistic Regression
                """
            )
            st.subheader("Speciality Trading")
            st.write(
                """
                * naive momentum
                * Pairs Correlation Trading
                * Support & Resistance
                * Turtle Trading
                * Mean Reversion & Trend Following
                * Volatility Mean Reversion & Trend Following
                * OverBought & OverSold
                """
            )
            st.subheader("Strategy Backtesting")
            st.write("* xgboost sim/backtesting")
            st.write("* backtrader backtesting")


    def run_movAvg_sma_ema(self, stock_ticker, data, sma_ema_opt, p_out=True, cc=0.0, ccc=0.0, inter='1d'):
        res, S, L = s1.optimal_2sma(stock_ticker).grab_data(self.today_stamp, data, inter)
        stock_symbol = s1.movAvg_sma_ema(stock_ticker, S, L, self.today_stamp, sma_ema_opt, data, p_out, cc, ccc, inter)        
        st.write('_'*25)
        if stock_symbol == stock_ticker:
            return True
        if stock_symbol != stock_ticker:
            return False
        else:
            return False
        

    def run_optimal_sma(self, stock_ticker, data, graphit=True, cc=0.0, ccc=0.0):
        stock_symbol = s1.optimal_sma(stock_ticker, self.today_stamp).build_optimal_sma(data, graphit, cc, ccc)
        st.write('_'*25)
        if stock_symbol == stock_ticker:
            return True
        if stock_symbol != stock_ticker:
            return False
        else:
            return False
        
    def run_indicators(self, stock_ticker, cc=0.0, ccc=0.0, graphit=True):
        stock_symbol = s1.ii(stock_ticker, cc, ccc, graphit).kingpsin()
        if stock_symbol == stock_ticker:
            return True
        if stock_symbol != stock_ticker:
            return False
        else:
            return False        



    def run_overBought_overSold(self, stock_ticker, data):
        st.write('_'*25)
        st.subheader(" > Over Bought & Over Sold Analysis ")
        s1.overBought_overSold(stock_ticker).generate(data)


    def run_supportResistance(self, stock_ticker):
        st.write('_'*25)
        st.subheader(" > Support & Resistance Lines ")
        s1.support_resistance(stock_ticker).level()


    def run_strategyII(self, stock_ticker):
        st.write('_'*25)
        st.subheader(" > Strategy II ")
        s1.Trading_Technicals(stock_ticker).trading_technicals()
