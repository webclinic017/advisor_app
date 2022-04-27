import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import math
import yfinance as yf
from matplotlib import pyplot as plt
from datetime import timedelta
import streamlit as st
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import plotly.express as px
import plotly.graph_objects as go

plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = [15, 10]
plt.rcParams["figure.dpi"] = 100

from src.tools import functions as f0




class Regression_Model(object):


    def __init__(self, ticker):
        self.ticker = ticker
        self.sName = f0.company_longName(self.ticker)


    def preprocessing(self):
        company_name = f0.company_longName(self.ticker)
        x = f"{company_name} [{self.ticker}]"
        st.subheader(f"𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄚𝄚 · {x} · 𝄚𝄚𝄙𝄙𝄘𝄘𝄗𝄗𝄖𝄖")
                
        df = yf.download(self.ticker, period="5y", parse_dates=True)
        dfreg = df.loc[:, ["Adj Close", "Volume"]]
        dfreg["HL_PCT"] = (df["High"] - df["Low"]) / df["Close"] * 100.0
        dfreg["PCT_change"] = (df["Close"] - df["Open"]) / df["Open"] * 100.0

        # Drop missing value
        dfreg.fillna(value=-99999, inplace=True)
        # We want to separate 1 percent of the data to forecast
        forecast_out = int(math.ceil(0.01 * len(dfreg)))
        # Separating the label here, we want to predict the AdjClose
        forecast_col = "Adj Close"
        dfreg["label"] = dfreg[forecast_col].shift(-forecast_out)
        X = np.array(dfreg.drop(["label"], 1))
        # Scale the X so that everyone can have the same distribution for linear regression
        X = sklearn.preprocessing.scale(X)
        # Finally We want to find Data Series of late X & early X (train) for model generation & eval
        X_lately = X[-forecast_out:]
        X = X[:-forecast_out]
        # Separate label and identify it as y
        y = np.array(dfreg["label"])
        y = y[:-forecast_out]
        X_train, X_test, y_train, y_test = train_test_split(X, y)

        # Linear regression
        clfreg = LinearRegression().fit(X_train, y_train)
        # Quadratic Regression 2
        clfpoly2 = make_pipeline(PolynomialFeatures(2), Ridge()).fit(X_train, y_train)
        # Quadratic Regression 3
        clfpoly3 = make_pipeline(PolynomialFeatures(3), Ridge()).fit(X_train, y_train)
        # KNN Regression
        clfknn = KNeighborsRegressor(n_neighbors=2).fit(X_train, y_train)

        # results
        confidencereg = clfreg.score(X_test, y_test)
        confidencepoly2 = clfpoly2.score(X_test, y_test)
        confidencepoly3 = clfpoly3.score(X_test, y_test)
        confidenceknn = clfknn.score(X_test, y_test)

        st.subheader(f"𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄚𝄚 Regression Analysis · Model Results ")
        st.write(f"▷ Linear Regression Confidence =  [{round(confidencereg * 100, 2)}%]")
        st.write(f"▷ Quadratic Regression 2 Confidence =  [{round(confidencepoly2 * 100, 2)}%]")
        st.write(f"▷ Quadratic Regression 3 Confidence =  [{round(confidencepoly3 * 100, 2)}%]")
        st.write(f"▷ KNN Regression Confidence =  [{round(confidenceknn * 100, 2)}%]")

        fd = pd.DataFrame()
        fd["---Regression_Model---"] = ["linear_regression", "quadratic_regression_2", "quadratic_regression_3", "knn"]
        fd["Model_Results"] = [confidencereg, confidencepoly2, confidencepoly3, confidenceknn]
        fd.set_index("---Regression_Model---", inplace=True)
        fd.sort_values("Model_Results", ascending=False, inplace=True)
        res_lst = [dfreg, X_lately, clfreg, clfpoly2, clfpoly3, clfknn, fd.index[0]]
        return res_lst


    def linear_regression(self, dfreg, X_lately, clfreg, clfpoly2, clfpoly3, clfknn, days=252):
        st.subheader(f"𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄚𝄚 Best Model Fit :  Linear Regression Forecast")
        forecast_set = clfreg.predict(X_lately)
        dfreg["Forecast"] = np.nan
        dfreg["Forecast"]
        last_date = dfreg.iloc[-1].name
        last_unix = last_date
        next_unix = last_unix + timedelta(1)
        for i in forecast_set:
            next_date = next_unix
            next_unix += timedelta(days)
            dfreg.loc[next_date] = [np.nan for _ in range(len(dfreg.columns) - 1)] + [i]
                        
        fig = go.Figure()
        df11 = dfreg.tail(134).copy()
        fig.add_scattergl(x=df11.index, y=df11["Forecast"], line={'color': 'blue'}, name="Forecast Line")
        fig.update_traces(mode='markers+lines')
        fig.add_scattergl(x=df11.index, y=df11["Adj Close"], line={'color': 'black'}, name="Close Line")
        fig.update_layout(    
            title="Portfolio Performance",
            title_font_color="royalblue",
            title_font_family="Times New Roman",
            xaxis_title="Days Since Bought Portfolio",    
            xaxis_title_font_color="darkred",    
            yaxis_title="Portfolio Value ($)",    
            yaxis_title_font_color="darkred",
            legend_title="Legend Title",
            legend_title_font_color="darkred",
            font=dict(family="Times New Roman",size=18,color="black"),
            width=1500, height=900
            )
        st.plotly_chart(fig, use_container_width=False, width=1500, height=900)

        fd = yf.download(self.ticker, period="1d")
        x = round(float(fd["Adj Close"]), 2)
        st.write(f" - {self.sName} · [{self.ticker}] · Current Stock Price = ${x}")
        x = dfreg["Forecast"].iloc[-1]
        st.write(f" - 1 year Forcasted Price = ${round(float(x),2)}")
        return


    def quadratic_regression_2(self, dfreg, X_lately, clfreg, clfpoly2, clfpoly3, clfknn, days=252):
        st.subheader(f"𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄚𝄚 Best Model Fit :  Quadratic-2 Regression Forecast")
        forecast_set = clfpoly2.predict(X_lately)
        dfreg["Forecast"] = np.nan
        dfreg["Forecast"]
        last_date = dfreg.iloc[-1].name
        last_unix = last_date
        next_unix = last_unix + timedelta(1)
        for i in forecast_set:
            next_date = next_unix
            next_unix += timedelta(days)
            dfreg.loc[next_date] = [np.nan for _ in range(len(dfreg.columns) - 1)] + [i]

        fig = go.Figure()
        df11 = dfreg.tail(134).copy()
        fig.add_scattergl(x=df11.index, y=df11["Forecast"], line={'color': 'blue'}, name="Forecast Line")
        fig.update_traces(mode='markers+lines')
        fig.add_scattergl(x=df11.index, y=df11["Adj Close"], line={'color': 'black'}, name="Close Line")
        fig.add_annotation(
            text="Absolutely-positioned annotation",
            xref="paper", yref="paper",
            x=df11.index[-5], 
            y=df11["Adj Close"].max()*0.95, 
            showarrow=False
            )        
        fig.update_layout(    
            title="Portfolio Performance",
            title_font_color="royalblue",
            title_font_family="Times New Roman",
            xaxis_title="Days Since Bought Portfolio",    
            xaxis_title_font_color="darkred",    
            yaxis_title="Portfolio Value ($)",    
            yaxis_title_font_color="darkred",
            legend_title="Legend Title",
            legend_title_font_color="darkred",
            font=dict(family="Times New Roman",size=18,color="black"),
            width=1500, height=900
            )
        # fig.update_layout(width=1500, height=900)
        st.plotly_chart(fig, use_container_width=False, width=1500, height=900)

        fd = yf.download(self.ticker, period="1d")
        x = round(float(fd["Adj Close"]), 2)
        st.write(f" - {self.sName} · [{self.ticker}] · Current Stock Price = ${x}")
        x = dfreg["Forecast"].iloc[-1]
        st.write(f" - 1 year Forcasted Price = ${round(float(x),2)}")
        return


    def quadratic_regression_3(self, dfreg, X_lately, clfreg, clfpoly2, clfpoly3, clfknn, days=252):
        st.subheader(f"𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄚𝄚 Best Model Fit :  Quadratic-3 Regression Forecast")
        forecast_set = clfpoly3.predict(X_lately)
        dfreg["Forecast"] = np.nan
        dfreg["Forecast"]
        last_date = dfreg.iloc[-1].name
        last_unix = last_date
        next_unix = last_unix + timedelta(1)
        for i in forecast_set:
            next_date = next_unix
            next_unix += timedelta(days)
            dfreg.loc[next_date] = [np.nan for _ in range(len(dfreg.columns) - 1)] + [i]
            
        fig = go.Figure()
        df11 = dfreg.tail(134).copy()
        fig.add_scattergl(x=df11.index, y=df11["Forecast"], line={'color': 'blue'}, name="Forecast Line")
        fig.update_traces(mode='markers+lines')
        fig.add_scattergl(x=df11.index, y=df11["Adj Close"], line={'color': 'black'}, name="Close Line")
        fig.add_annotation(
            text="Absolutely-positioned annotation",
            xref="paper", yref="paper",
            x=df11.index[-5], 
            y=df11["Adj Close"].max()*0.95, 
            showarrow=False
            )        
        fig.update_layout(    
            title="Portfolio Performance",
            title_font_color="royalblue",
            title_font_family="Times New Roman",
            xaxis_title="Days Since Bought Portfolio",    
            xaxis_title_font_color="darkred",    
            yaxis_title="Portfolio Value ($)",    
            yaxis_title_font_color="darkred",
            legend_title="Legend Title",
            legend_title_font_color="darkred",
            font=dict(family="Times New Roman",size=18,color="black"),
            width=1500, height=900
            )
        # fig.update_layout(width=1500, height=900)
        st.plotly_chart(fig, use_container_width=False, width=1500, height=900)

        fd = yf.download(self.ticker, period="1d")
        x = round(float(fd["Adj Close"]), 2)
        st.write(f" - {self.sName} · [{self.ticker}] · Current ticker Price = ${x}")
        x = dfreg["Forecast"].iloc[-1]
        st.write(f" - 1 year Forcasted Price = ${round(float(x),2)}")
        return


    def knn(self, dfreg, X_lately, clfreg, clfpoly2, clfpoly3, clfknn, days=252):
        st.subheader(f"𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄚𝄚 Best Model Fit :  KNN Regression Forecast")
        forecast_set = clfknn.predict(X_lately)
        dfreg["Forecast"] = np.nan
        dfreg["Forecast"]
        last_date = dfreg.iloc[-1].name
        last_unix = last_date
        next_unix = last_unix + timedelta(1)
        for i in forecast_set:
            next_date = next_unix
            next_unix += timedelta(days)
            dfreg.loc[next_date] = [np.nan for _ in range(len(dfreg.columns) - 1)] + [i]
            
        fig = go.Figure()
        df11 = dfreg.tail(134).copy()
        fig.add_scattergl(x=df11.index, y=df11["Forecast"], line={'color': 'blue'}, name="Forecast Line")
        fig.update_traces(mode='markers+lines')
        fig.add_scattergl(x=df11.index, y=df11["Adj Close"], line={'color': 'black'}, name="Close Line")        
        fig.add_annotation(
            text="Absolutely-positioned annotation",
            xref="paper", yref="paper",
            x=df11.index[-5], 
            y=df11["Adj Close"].max()*0.95, 
            showarrow=False
            )        
        fig.update_layout(    
            title="Portfolio Performance",
            title_font_color="royalblue",
            title_font_family="Times New Roman",
            xaxis_title="Days Since Bought Portfolio",    
            xaxis_title_font_color="darkred",    
            yaxis_title="Portfolio Value ($)",    
            yaxis_title_font_color="darkred",
            legend_title="Legend Title",
            legend_title_font_color="darkred",
            font=dict(family="Times New Roman",size=18,color="black"),
            width=1500, height=900
            )
        # fig.update_layout(width=1500, height=900)
        st.plotly_chart(fig, use_container_width=False, width=1500, height=900)

        fd = yf.download(self.ticker, period="1d")
        x = round(float(fd["Adj Close"]), 2)
        st.write(f" - {self.sName} · [{self.ticker}] · Current Stock Price = ${x}")
        x = dfreg["Forecast"].iloc[-1]
        st.write(f" - 1 year Forcasted Price = ${round(float(x),2)}")
        return
