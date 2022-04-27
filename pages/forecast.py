import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, date, timedelta
from yahooquery import Ticker, ticker
import matplotlib.pyplot as plt

from src.tools import functions as f0
from src.tools import lists as l0
from src.tools import scripts as s0
from src.tools import widgets as w0
import src.models.forecast as f1

plt.style.use("ggplot")
# sm, med, lg = "20", "25", "30"
# plt.rcParams["font.size"] = sm  # controls default text sizes
# plt.rc("axes", titlesize=med)  # fontsize of the axes title
# plt.rc("axes", labelsize=med)  # fontsize of the x & y labels
# plt.rc("xtick", labelsize=sm)  # fontsize of the tick labels
# plt.rc("ytick", labelsize=sm)  # fontsize of the tick labels
# plt.rc("legend", fontsize=sm)  # legend fontsize
# plt.rc("figure", titlesize=lg)  # fontsize of the figure title
# plt.rc("axes", linewidth=2)  # linewidth of plot lines
# plt.rcParams["figure.figsize"] = [15, 13]
# plt.rcParams["figure.dpi"] = 113
# plt.rcParams["axes.facecolor"] = "silver"


casting_periods = [21, 63, 126, 252, 378, 504]

prophet_url = "https://facebook.github.io/prophet/docs/quick_start.html#python-api"
prophet_script_1 = "\n\
- Prophet is a procedure for forecasting time series data based on an additive model where \
    non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects."
prophet_script_2 = "\n\
- It works best with time series that have strong seasonal effects and several seasons of historical data. \
    Prophet is robust to missing data and shifts in the trend, and typically handles outliers well."


univariate_script = f"\
    * The term 'univariate' implies that forecasting is based on a sample of time series \
    observations of the exchange rate without taking into account the effect of the other \
    variables such as prices and interest rates. If this is the case, then there is no need \
    to take an explicit account of these variables."


class Forecast(object):
    def __init__(self, today_stamp):
        self.today_stamp = today_stamp
        self.saveMonth = str(datetime.now())[:7]
        self.saveDay = str(datetime.now())[8:10]

        self.saveRec = Path(f"data/recommenders/{str(today_stamp)[:4]}/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveRec.exists():
            self.saveRec.mkdir(parents=True)

        self.saveRaw = Path(f"data/raw/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveRaw.exists():
            self.saveRaw.mkdir(parents=True)

        self.saveScreeners = Path(f"data/screeners/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveScreeners.exists():
            self.saveScreeners.mkdir(parents=True)

        self.saveTickers = Path(f"data/tickers/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveTickers.exists():
            self.saveTickers.mkdir(parents=True)


    def prophet(self, ticker_list):
        st.header("𝄖𝄖𝄖𝄖𝄖𝄗𝄗𝄗𝄗𝄘𝄘𝄘𝄙𝄙𝄚 ▷ Prophet ◁ 𝄚𝄙𝄙𝄘𝄘𝄘𝄗𝄗𝄗𝄗𝄖𝄖𝄖𝄖𝄖")
        cols = st.columns(2)
        with cols[0]:       
            with st.expander("▷ Details:", expanded=False):         
                clicked = w0.widget_prophet(prophet_script_1, prophet_script_2, prophet_url)
        st.header(f"{'𝄖'*33}")        
        ender_date = str(st.sidebar.date_input("[ 4 ] Forecast Start Date", datetime(2022, 1, 1)))[:10]
        prophet_period_1 = st.sidebar.selectbox("[ 5 ] Forcast Period (DAYS)", casting_periods, index=2)
        if st.sidebar.button("[ 6 ] RUN PROPHET FORECAST"):
            if type(self.one_er_many) == str:
                for r in ticker_list:
                    f1.prophet(r, ender_date, prophet_period_1, hist="2y").run_prophet()
            elif type(self.one_er_many) == int:
                f1.prophet(ticker_list, ender_date, prophet_period_1, hist="2y").run_prophet()


    def mc_forecast(self, ticker_list):
        st.header("𝄖𝄖𝄖𝄖𝄖𝄗𝄗𝄗𝄗𝄘𝄘𝄘𝄙𝄙𝄚 ▷ Monte Carlo Cholesky ◁ 𝄚𝄙𝄙𝄘𝄘𝄘𝄗𝄗𝄗𝄗𝄖𝄖𝄖𝄖𝄖")
        st.header(f"{'𝄖'*33}")
        forecast_days = st.sidebar.selectbox("[ 4 ] Forcast Period (DAYS)", casting_periods, index=2)
        if st.sidebar.button("[ 5 ] Run Monte Carlo Sim Forecast"):
            f1.MC_Forecast().monte_carlo(
                tickers=ticker_list,
                days_forecast=forecast_days,
                iterations=13000,
                start_date="2010-01-01",
                return_type="log",
                plotten=False,
                )


    def stocker(self, ticker_list):
        st.header("𝄖𝄖𝄖𝄖𝄖𝄗𝄗𝄗𝄗𝄘𝄘𝄘𝄙𝄙𝄚 ▷ Stocker ◁ 𝄚𝄙𝄙𝄘𝄘𝄘𝄗𝄗𝄗𝄗𝄖𝄖𝄖𝄖𝄖")
        st.header(f"{'𝄖'*33}")        
        stocker_forcast_period = st.sidebar.selectbox("[ 4 ] Forcast Period (DAYS)", casting_periods, index=2)
        e_date = str(st.sidebar.date_input("[ 5 ] Forecast Start Date", datetime(2022, 1, 1)))[:10]
        if st.sidebar.button("[ 6 ] RUN STOCKER FORECAST"):
            if type(self.one_er_many) == str:
                for r in ticker_list:
                    f1.web_stocker_run(r, stocker_forcast_period, e_date)
            elif type(self.one_er_many) == int:
                f1.web_stocker_run(ticker_list, stocker_forcast_period, e_date)


    def regression(self, ticker_list):
        st.header("𝄖𝄖𝄖𝄖𝄖𝄗𝄗𝄗𝄗𝄘𝄘𝄘𝄙𝄙𝄚 ▷ Regression ◁ 𝄚𝄙𝄙𝄘𝄘𝄘𝄗𝄗𝄗𝄗𝄖𝄖𝄖𝄖𝄖")
        st.header(f"{'𝄖'*33}")               
        if st.sidebar.button("[ 4 ] RUN REGRESSION FORECAST"):
            days = 5
            if type(ticker_list) == list:
                for stock_ticker in ticker_list:
                    (dfreg, X_lately, clfreg, clfpoly2, clfpoly3, clfknn, modName) = f1.regression(stock_ticker).preprocessing()
                    if modName == "linear_regression":
                        f1.regression(stock_ticker).linear_regression(dfreg, X_lately, clfreg, clfpoly2, clfpoly3, clfknn, days)
                    if modName == "quadratic_regression_2":
                        f1.regression(stock_ticker).quadratic_regression_2(dfreg, X_lately, clfreg, clfpoly2, clfpoly3, clfknn, days)
                    if modName == "quadratic_regression_3":
                        f1.regression(stock_ticker).quadratic_regression_3(dfreg, X_lately, clfreg, clfpoly2, clfpoly3, clfknn, days)
                    if modName == "knn":
                        f1.regression(stock_ticker).knn(dfreg, X_lately, clfreg, clfpoly2, clfpoly3, clfknn, days)
            else:
                (dfreg, X_lately, clfreg, clfpoly2, clfpoly3, clfknn, modName) = f1.regression(ticker_list).preprocessing()
                if modName == "linear_regression":
                    f1.regression(ticker_list).linear_regression(dfreg, X_lately, clfreg, clfpoly2, clfpoly3, clfknn, days)
                if modName == "quadratic_regression_2":
                    f1.regression(ticker_list).quadratic_regression_2(dfreg, X_lately, clfreg, clfpoly2, clfpoly3, clfknn, days)
                if modName == "quadratic_regression_3":
                    f1.regression(ticker_list).quadratic_regression_3(dfreg, X_lately, clfreg, clfpoly2, clfpoly3, clfknn, days)
                if modName == "knn":
                    f1.regression(ticker_list).knn(dfreg, X_lately, clfreg, clfpoly2, clfpoly3, clfknn, days)


    def sarima(self, ticker_list):
        st.header("𝄖𝄖𝄖𝄖𝄖𝄗𝄗𝄗𝄗𝄘𝄘𝄘𝄙𝄙𝄚 ▷ SARIMA ◁ 𝄚𝄙𝄙𝄘𝄘𝄘𝄗𝄗𝄗𝄗𝄖𝄖𝄖𝄖𝄖")
        st.caption("* Seasonal AutoRegressive Integrated Moving Average")
        st.header(f"{'𝄖'*33}")                      
        if st.sidebar.button("[ 4 ] RUN SARIMA FORECAST"):
            if type(ticker_list) == list:
                for stock_ticker in ticker_list:
                    f1.sarima(stock_ticker).predict()
                    st.write(" *" * 25)
            if type(ticker_list) == str:
                f1.sarima(ticker_list).predict()
                st.write(" *" * 25)
                

    def arima(self, ticker_list):
        st.header("𝄖𝄖𝄖𝄖𝄖𝄗𝄗𝄗𝄗𝄘𝄘𝄘𝄙𝄙𝄚 ▷ ARIMA ◁ 𝄚𝄙𝄙𝄘𝄘𝄘𝄗𝄗𝄗𝄗𝄖𝄖𝄖𝄖𝄖")
        st.caption("* Auto Regression Integrated Moving Average")
        st.header(f"{'𝄖'*33}")
        if st.sidebar.button("[ 4 ] RUN ARIMA FORECAST"):
            if type(ticker_list) == list:
                for stock_ticker in ticker_list:
                    f1.arima1(stock_ticker).arima_model()
                    f1.arima2(stock_ticker).runArima()
            if type(ticker_list) == str:
                f1.arima1(ticker_list).arima_model()
                f1.arima2(stock_ticker).runArima()


    def monte_carlo(self, ticker_list):
        st.header("𝄖𝄖𝄖𝄖𝄖𝄗𝄗𝄗𝄗𝄘𝄘𝄘𝄙𝄙𝄚 ▷ Monte Carlo Simulations ◁ 𝄚𝄙𝄙𝄘𝄘𝄘𝄗𝄗𝄗𝄗𝄖𝄖𝄖𝄖𝄖")
        cols = st.columns(2)
        with cols[0]:       
            with st.expander("▷ Details:"): 
                st.caption(
                    f"\
                    * A Monte Carlo simulation is a useful tool for predicting future results calculating \
                        a formula multiple times with different random inputs. \n\
                    ")
        st.header(f"{'𝄖'*33}")        
        if st.sidebar.button("[ 4 ] RUN MONTE CARLO FORECAST"):
            for stock_ticker in ticker_list:
                f1.monteCarlo(stock_ticker).creation_B()
                # st.write(" *" * 25)
                # f1.monteCarlo(stock_ticker).creation_A()
                
                
    def univariate(self, ticker_list):
        st.header("𝄖𝄖𝄖𝄖𝄖𝄗𝄗𝄗𝄗𝄘𝄘𝄘𝄙𝄙𝄚 ▷ Univariate RNN ◁ 𝄚𝄙𝄙𝄘𝄘𝄘𝄗𝄗𝄗𝄗𝄖𝄖𝄖𝄖𝄖")
        cols = st.columns(2)
        with cols[0]:
            with st.expander("▷ Details:"):
                clicked = w0.widget_univariate(univariate_script)
        st.header(f"{'𝄖'*33}")
        if st.sidebar.button("[ 4 ] RUN UNIVARIATE FORECAST"):
            if type(self.one_er_many) == str:
                for stock_ticker in ticker_list:
                    f1.univariate_1(stock_ticker).runs()
            elif type(self.one_er_many) == int:
                f1.univariate_1(ticker_list).runs()

    # ------------------------------------------------------------------------------------------ > stage: [FORECAST]

    def run_forecast(self):
        st.header("◾ 𝄖𝄖𝄖𝄗𝄗𝄗𝄘𝄘𝄙𝄙𝄚 · Forecasting · 𝄚𝄙𝄙𝄘𝄘𝄗𝄗𝄗𝄖𝄖𝄖 ◾")
        st.header(f"{' '*25}")
        

        self.one_er_many = "List"
        st.sidebar.write("\
            - NOTE: all models take time to run \n\
            - Careful using with too many tickers \n\
            "
        )
        
        model = st.sidebar.selectbox("[ 2 ] Select Model:", l0.feature_forecast)
        
        personal_stocks = st.sidebar.text_input("[ 3 ] Enter Stock", value="AAPL")
        personal_stocks = personal_stocks.split()        

        if model == "Prophet Model":
            self.prophet(personal_stocks)
            st.subheader("𝄖𝄗𝄘𝄙𝄚 Forecast Complete")

        if model == "Stocker Analysis":
            self.stocker(personal_stocks)
            st.subheader("𝄖𝄗𝄘𝄙𝄚 Forecast Complete")

        if model == "SARIMA":
            self.sarima(personal_stocks)
            st.subheader("𝄖𝄗𝄘𝄙𝄚 Forecast Complete")
            
        if model == "Monte Carlo Cholesky":
            self.mc_forecast(personal_stocks)      
            st.subheader("𝄖𝄗𝄘𝄙𝄚 Forecast Complete")      

        if model == "Monte Carlo Simulation":
            self.monte_carlo(personal_stocks)
            st.subheader("𝄖𝄗𝄘𝄙𝄚 Forecast Complete")

        if model == "Univariate Analysis":
            self.univariate(personal_stocks)
            st.subheader("𝄖𝄗𝄘𝄙𝄚 Forecast Complete")
            
        if model == "Regression":
            self.regression(personal_stocks)       
            st.subheader("𝄖𝄗𝄘𝄙𝄚 Forecast Complete")     

        if model == "ARIMA":
            self.arima(personal_stocks)
            st.subheader("𝄖𝄗𝄘𝄙𝄚 Forecast Complete")