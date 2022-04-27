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
        
        st.header("⬛ 𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄚𝄚𝄚 · Strategy · 𝄚𝄚𝄚𝄙𝄙𝄘𝄘𝄗𝄗𝄖𝄖 ⬛")
        st.header(f"{' '*25}")
        st.header(f"{'𝄗'*32}")        


    def run_the_strats(self):
        select_stocks = st.sidebar.selectbox("[ 2 ] Select Stock", ("Single Stock", "Multiple Stocks"))
        
        if select_stocks == "Single Stock":
            method_strat = st.sidebar.selectbox("[ 3 ] Select Method", ("Individual Strategy", "Run All Strategies"))
            model = st.sidebar.selectbox("[ 4 ] Select Model", l0.feature_strategy, index=0)
            
            if method_strat == "Run All Strategies":
                st.sidebar.write(" *" * 25)            
                if st.sidebar.button("Run Strategies"):
                    self.run_movAvg_sma_ema(self.stock_ticker)
                    self.run_optimal_sma(self.stock_ticker)
                    self.run_overBought_overSold(self.stock_ticker)
                    self.run_supportResistance(self.stock_ticker)
                    self.run_strategyII(self.stock_ticker)


            if method_strat == "Individual Strategy":
                self.stock_ticker = st.sidebar.text_input(label="[ 5 ] Enter Stock In ALL CAPS [example: TSLA]", value="TSLA")

                if model == "-Select-Model-":
                    self.run_homePage()
                    
                else:
                    if st.sidebar.button("[ 6 ] Implement Strategy"):

                        if model == "Moving-Average":
                            st.sidebar.write("__" * 25)
                            self.run_movAvg_sma_ema(self.stock_ticker)

                        if model == "Optimal SMA":
                            self.run_optimal_sma(self.stock_ticker)

                        if model == "OverBought & OverSold":
                            self.run_overBought_overSold(self.stock_ticker)

                        if model == "Support & Resistance Lines":
                            self.run_supportResistance(self.stock_ticker)

                        if model == "Strategy II":
                            self.run_strategyII(self.stock_ticker)
                            
                        if model == "Indicators":
                            self.run_indicators(self.stock_ticker)



        if select_stocks == "Multiple Stocks":
            st.sidebar.write(" *" * 25)
            stock_ticker = st.sidebar.text_input(
                label="Enter Your Own Stock List To Model The various Machine Learning & Algo Trading Strategies",
                value="TSLA NVDA AAPL ASML SNOW",
            )
            stock_ticker = stock_ticker.split()
            st.sidebar.write(" *" * 25)
            

            method_strat = "Individual Strategy"
            if method_strat == "Individual Strategy":
                model = st.sidebar.radio("[ 5 ] Select Model", l0.feature_strategy)
                st.sidebar.write(" *" * 25)               

                if model == "Moving-Average - SMA & EMA":
                    st.sidebar.write("__" * 25)
                    if st.sidebar.button("Run Strategies", key='b'):         
                                                
                        for s in stock_ticker:
                            self.run_movAvg_sma_ema(s)

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


    def run_movAvg_sma_ema(self, stock_ticker, cc=0.0, ccc=0.0, inter='1d'):
        st.header("𝄖𝄗𝄘𝄙𝄙𝄚𝄚 Optimal Double Moving Average 𝄚𝄚𝄙𝄙𝄘𝄗𝄖")
        st.header(f"{' '*25}")
        st.header(f"{'𝄖'*32}") 
        S, L = s1.optimal_2sma(stock_ticker).grab_data(self.today_stamp, inter)
        s1.movAvg_sma_ema(stock_ticker, S, L, self.today_stamp, 'SMA', cc, ccc, inter)
        st.write('*'*34)
        s1.movAvg_sma_ema(stock_ticker, S, L, self.today_stamp, 'EWMA', cc, ccc, inter)
        st.subheader("𝄖𝄗𝄘𝄙𝄚 Strategy Complete")
        

    def run_optimal_sma(self, stock_ticker, graphit=True, cc=0.0, ccc=0.0):
        st.header("𝄖𝄗𝄘𝄙𝄙𝄚𝄚 Optimal Single Moving Averages 𝄚𝄚𝄙𝄙𝄘𝄗𝄖")
        st.header(f"{' '*25}")
        st.header(f"{'𝄖'*32}")         
        s1.optimal_sma(stock_ticker, self.today_stamp).build_optimal_sma(graphit, cc, ccc)
        st.subheader("𝄖𝄗𝄘𝄙𝄚 Strategy Complete")

        
    def run_indicators(self, stock_ticker):
        st.header("𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄚𝄚 Indicator Analysis 𝄚𝄚𝄙𝄙𝄘𝄘𝄗𝄗𝄖𝄖")
        st.header(f"{' '*25}")
        st.header(f"{'𝄖'*32}")        
        s1.Indicator_Ike(stock_ticker).kingpin()
        st.subheader("𝄖𝄗𝄘𝄙𝄚 Strategy Complete")


    def run_overBought_overSold(self, stock_ticker):
        st.header("𝄖𝄗𝄘𝄙𝄙𝄚𝄚 Over Bought & Over Sold Analysis 𝄚𝄚𝄙𝄙𝄘𝄗𝄖")
        st.header(f"{' '*25}")
        st.header(f"{'𝄖'*32}")              
        s1.overBought_overSold(stock_ticker).generate()
        st.subheader("𝄖𝄗𝄘𝄙𝄚 Strategy Complete")


    def run_supportResistance(self, stock_ticker):
        st.header("𝄖𝄗𝄘𝄙𝄙𝄚𝄚 Support & Resistance Analysis 𝄚𝄚𝄙𝄙𝄘𝄗𝄖")
        st.header(f"{' '*25}")
        st.header(f"{'𝄖'*32}")
        s1.support_resistance(stock_ticker).level()
        st.subheader("𝄖𝄗𝄘𝄙𝄚 Strategy Complete")


    def run_strategyII(self, stock_ticker):
        st.header("𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄚𝄚 Strategy II Analysis 𝄚𝄚𝄙𝄙𝄘𝄘𝄗𝄗𝄖𝄖")
        st.header(f"{' '*25}")
        st.header(f"{'𝄖'*32}")
        s1.Trading_Technicals(stock_ticker).trading_technicals()
        st.subheader("𝄖𝄗𝄘𝄙𝄚 Strategy Complete")
