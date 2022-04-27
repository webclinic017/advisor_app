import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.filterwarnings("ignore")

import streamlit as st
st.set_option("deprecation.showPyplotGlobalUse", False)

from datetime import date, datetime
import numpy as np
import pandas as pd
import yfinance as yf

import pyfolio as pf
import src.tools.functions as f0
from src.models.backtest.A1 import (calc_moving_average, get_ticker_data, ma_backtest, plot)
from src.models.backtest.optimal_double_mavg import Optimal_Double_Mavg_Crossover
from src.models.backtest.optimal_sma import Optimal_SMA

import matplotlib.pyplot as plt
pd.plotting.register_matplotlib_converters()
plt.style.use("ggplot")
sm, med, lg = "20", "25", "30"
plt.rcParams["font.size"] = sm                                        # controls default text sizes
plt.rc("axes", titlesize=med)                                         # fontsize of the axes title
plt.rc("axes", labelsize=med)                                         # fontsize of the x & y labels
plt.rc("xtick", labelsize=sm)                                         # fontsize of the tick labels
plt.rc("ytick", labelsize=sm)                                         # fontsize of the tick labels
plt.rc("legend", fontsize=sm)                                         # legend fontsize
plt.rc("figure", titlesize=lg)                                        # fontsize of the figure title
plt.rc("axes", linewidth=2)                                           # linewidth of plot lines
plt.rcParams["figure.figsize"] = [10, 7]
plt.rcParams["figure.dpi"] = 100
plt.rcParams["axes.facecolor"] = "silver"




class Backtest(object):

    def __init__(self):
        self.today_stamp = str(datetime.now())[:10]
        st.header("⬛ 𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄚𝄚 · Backtesting · 𝄚𝄚𝄙𝄙𝄘𝄘𝄗𝄗𝄖𝄖 ⬛")
        st.header(f"{' '*25}")
        st.header(f"{'𝄗'*32}")        


    def backtest_1(self):
        method = st.sidebar.selectbox("[ 2 ] SELECT METHOD: ", ["Single Ticker", "Portfolio"])

        if method == "Single Ticker":
            mode = st.sidebar.selectbox("[ 3 ] SELECT MODE:", ["Pyfolio", "Strategy Comparrison"])


            if mode == "Pyfolio":
                st.header("𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄙𝄚𝄚𝄚 Pyfolio Analysis 𝄚𝄚𝄚𝄙𝄙𝄙𝄘𝄘𝄗𝄗𝄖𝄖")
                st.header(f"{' '*25}")
                st.header(f"{'𝄖'*32}")
                                
                stock_ticker = st.sidebar.text_input("[ 4 ] SELECT TICKER:", "NVDA")
                if st.sidebar.button("[ 5 ] Run Pyfolio"):
                    stock_rets = pf.utils.get_symbol_rets(stock_ticker)
                    st.pyplot(pf.create_returns_tear_sheet(stock_rets, live_start_date="2020-12-30"))
                    st.pyplot(pf.create_full_tear_sheet(stock_rets, live_start_date="2020-12-30"))


            if mode == "Strategy Comparrison":
                """
                * filter moving average windows by strategy
                """
                self.ticker = st.sidebar.text_input("[ 4 ] SELECT TICKER:", "NVDA")
                self.strategy = st.sidebar.selectbox("[ 5 ] SELECT STRATEGY:", ["Single Moving Average", "Double Moving Average Crossover"], index=1)
                self.hist_per = "1y" # "3mo", "6mo", "ytd", "1y", "2y", "5y", "10y", "max"
                self.sellShort = False
                mod_01 = 'Auto Optimize' # 'Set Inputs'
                
                
                st.header("𝄖𝄗𝄘𝄙𝄙𝄚𝄚 Strategy Comparrison Analysis 𝄚𝄚𝄙𝄙𝄘𝄗𝄖")
                st.header(f"{' '*25}")
                st.header(f"{'𝄖'*32}")
                        
                company_name = f0.company_longName(self.ticker)
                x = f"{company_name} [{self.ticker}]"
                st.subheader(f"𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄙𝄚𝄚𝄚 {x} 𝄚𝄚𝄚𝄙𝄙𝄙𝄘𝄘𝄗𝄗𝄖𝄖")               


                if self.strategy == "Single Moving Average":
                    if mod_01 == 'Set Inputs':single_ma = st.sidebar.number_input(label='set single sma', value=20)

                    if st.sidebar.button("[ 6 ] Run Backtest"):
                        if mod_01 == 'Auto Optimize':
                            single_ma = Optimal_SMA(self.ticker, self.hist_per).build_optimal_sma()

                        single_ma = [single_ma]
                        strategy = "Single Moving Average"
                        window = single_ma
                        data = get_ticker_data(self.ticker, self.hist_per)
                        data = calc_moving_average(data, self.ticker, window)
                        sma_trade = ma_backtest(data, window, strategy, self.sellShort)
                        plot(sma_trade, self.ticker, window, strategy)
                        strategy_return = sma_trade.Cumulative[-1]
                        buy_hold = (sma_trade["close"][-1] - sma_trade.close[0]) / sma_trade["close"][0]

                        if strategy_return > buy_hold:
                            st.success("Best Performing Strategy: SINGLE EMA {:.2%}".format(sma_trade.Cumulative[-1]))
                            st.info("Performance: Buy & Hold Strategy {:.2%}".format((sma_trade.close[-1] - sma_trade.close[0])/ sma_trade.close[0]))
                        else:
                            st.info("Performance: SINGLE EMA Strategy {:.2%}".format(sma_trade.Cumulative[-1]))
                            st.success("Best Performing Strategy: BUY & HOLD {:.2%}".format((sma_trade.close[-1] - sma_trade.close[0])/ sma_trade.close[0]))


                if self.strategy == "Double Moving Average Crossover":
                    if mod_01 == 'Set Inputs':
                        Short = st.sidebar.number_input(label='set Short sma',value=20)
                        Long = st.sidebar.number_input(label='set Long sma',value=50)                        

                    if st.sidebar.button("[ 6 ] Run Backtest"):
                        company_longName = f0.company_longName(self.ticker)
                        if mod_01 == 'Auto Optimize':
                            Short, Long = Optimal_Double_Mavg_Crossover(self.ticker, company_longName).grab_data(self.hist_per)                        

                        sma = Short
                        lma = Long
                        strategy = "Crossover Moving Average"
                        window = [sma, lma]
                        data = get_ticker_data(self.ticker, self.hist_per)
                        data = calc_moving_average(data, self.ticker, window)
                        sma_trade = ma_backtest(data, window, strategy, sellShort=False)
                        plot(sma_trade, self.ticker, window, strategy)
                        strategy_return = sma_trade.Cumulative[-1]
                        buy_hold = (sma_trade.close[-1] - sma_trade.close[0]) / sma_trade.close[0]

                        if strategy_return > buy_hold:
                            st.success("Percent return on this strategy would have been {:.2%}".format(sma_trade.Cumulative[-1]))
                            st.info("Percent return on buy and hold would have been {:.2%}".format((sma_trade.close[-1] - sma_trade.close[0])/ sma_trade.close[0]))
                        else:
                            st.info("Percent return on this strategy would have been {:.2%}".format(sma_trade.Cumulative[-1]))
                            st.success("Percent return on buy and hold would have been {:.2%}".format((sma_trade.close[-1] - sma_trade.close[0])/ sma_trade.close[0]))

        if method == "Portfolio":
            opts = ["4M Portfolios", "Your Own"]
            version = st.sidebar.selectbox("Select Version", opts)

            if version == "Your Own":
                portfolio = st.sidebar.text_input("TICKERS ONLY", "NVDA AAPL AMZN GOOGL FB MSFT")

                if st.sidebar.button("Run Portfolio Birds Eye"):
                    RISKY_ASSETS = portfolio.split()
                    START_DATE = "2017-01-01"
                    END_DATE = "2021-10-01"
                    n_assets = len(RISKY_ASSETS)

                    prices_df = yf.download(RISKY_ASSETS, start=START_DATE, end=END_DATE, adjusted=True)

                    print(f"Downloaded {prices_df.shape[0]} rows of data.")
                    returns = prices_df["Adj Close"].pct_change().dropna()
                    portfolio_weights = n_assets * [1 / n_assets]
                    portfolio_returns = pd.Series(np.dot(portfolio_weights, returns.T), index=returns.index)
                    st.pyplot(pf.create_simple_tear_sheet(portfolio_returns))
                    st.pyplot(pf.create_returns_tear_sheet(portfolio_returns))
                    st.pyplot(pf.create_full_tear_sheet(portfolio_returns))

            if version == "4M Portfolios":
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
                name_lst = st.sidebar.selectbox(
                    label="", 
                    options=(
                        'markowitz_random',
                        'minimum_volatility_portfolio',    
                        'maximum_sharpe_ratio',
                        'minimum_volatility_random',
                        'maximum_sharpe_equalWT',
                        'monte_carlo_cholesky',
                    )
                )
                ticker_list = f0.recommended_stocks_2(name_lst, report_date)                
                st.write(f" * Portfolio Components: [{len(ticker_list)} Tickers]")
                st.write(f"{'_'*25} \n {'_'*25}")

                RISKY_ASSETS = ticker_list
                START_DATE = "2021-01-04"
                END_DATE = str(date.today())[:10]
                n_assets = len(RISKY_ASSETS)


                if st.sidebar.button("Run Portfolio Birds Eye"):
                    prices_df = yf.download(RISKY_ASSETS, start=START_DATE, end=END_DATE)
                    print(f"Downloaded {prices_df.shape[0]} rows of data.")

                    returns = prices_df["Adj Close"].pct_change().dropna()
                    portfolio_weights = n_assets * [1 / n_assets]
                    portfolio_returns = pd.Series(np.dot(portfolio_weights, returns.T), index=returns.index)

                    st.pyplot(pf.create_simple_tear_sheet(portfolio_returns))
                    st.pyplot(pf.create_returns_tear_sheet(portfolio_returns))
                    st.pyplot(pf.create_full_tear_sheet(portfolio_returns))
