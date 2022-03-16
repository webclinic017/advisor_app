import numpy as np
import warnings
warnings.filterwarnings("ignore")
import talib as ta
import yfinance as yf
import matplotlib.pyplot as plt 
from datetime import datetime
import matplotlib.dates as mdates
from yahooquery import Ticker
import pandas as pd
import streamlit as st

plt.style.use('seaborn-talk')
sm, med, lg = 10, 15, 20
plt.rc("font", size=sm)  # controls default text sizes
plt.rc("axes", titlesize=med)  # fontsize of the axes title
plt.rc("axes", labelsize=med)  # fontsize of the x & y labels
plt.rc("xtick", labelsize=sm)  # fontsize of the tick labels
plt.rc("ytick", labelsize=sm)  # fontsize of the tick labels
plt.rc("legend", fontsize=sm)  # legend fontsize
plt.rc("figure", titlesize=lg)  # fontsize of the figure title
plt.rc("axes", linewidth=2)  # linewidth of plot lines
plt.rcParams["figure.figsize"] = [15, 8]
plt.rcParams["figure.dpi"] = 100


def get_company_longName(symbol):
    d = Ticker(symbol).quote_type
    return list(d.values())[0]["longName"]




class Indicator_Ike(object):
    
    
    def __init__(self, ticker, date1, cc=0.0, ccc=0.0, graphit=True):
        self.stock = ticker
        self.date1 = date1
        self.cc = cc
        self.ccc = ccc
        self.graphit = graphit
        
         
    def get_data(self):
        data = yf.download(self.stock, period='2y')
        self.data = data.loc[:self.date1]
        return self.data
        
        
    def bollinger_bands(self, df):
        df['upper_band'], df['middle_band'], df['lower_band'] = ta.BBANDS(df['Close'], timeperiod =20)
        df["Signal"] = 0.0
        df["Signal"] = np.where(df['Close'] > df['middle_band'], 1.0, 0.0)
        df["Position"] = df["Signal"].diff()
        df_pos = df[(df["Position"] == 1) | (df["Position"] == -1)]
        df_pos["Position"] = df_pos["Position"].apply(lambda x: "Buy" if x == 1 else "Sell")       
        
        if self.graphit is True:
            fig, ax = plt.subplots()
            plt.tick_params(axis="both", labelsize=15)        
            df['Close'].plot(color="k", lw=2, label='Close')
            df['upper_band'].plot(color="g", lw=1, label='upper_band', linestyle='dashed')
            df['middle_band'].plot(color="r", lw=1, label='middle_band')
            df['lower_band'].plot(color="b", lw=1, label='lower_band', linestyle='dashed')
            # plot 'buy' signals
            plt.plot(
                df[df["Position"] == 1].index,
                df['Close'][df["Position"] == 1],
                "^", markersize=15, color="g", alpha=0.7, label="buy",
            )
            # plot 'sell' signals
            plt.plot(
                df[df["Position"] == -1].index,
                df['Close'][df["Position"] == -1],
                "v", markersize=15, color="r", alpha=0.7, label="sell",
            )        
            plt.ylabel("Price", fontsize=20, fontweight="bold")
            plt.xlabel("Date", fontsize=20, fontweight="bold")
            plt.title(f"{self.stock} - bollinger bands", fontsize=30, fontweight="bold")
            plt.grid(True, color="k", linestyle="-", linewidth=1, alpha=0.3)
            ax.legend(loc="best", prop={"size": 16})
            plt.tight_layout()
            plt.show()
            st.pyplot(fig)
        
        if df_pos['Position'][-1] == 'Buy':
            st.metric(f"No. {self.cc} / {self.ccc} In Portfolio", f"{self.stock}", f"{df_pos['Position'][-1]}");
            return self.stock
        elif df_pos['Position'][-1] == 'Sell':
            st.metric(f"No. {self.cc} / {self.ccc} In Portfolio", f"{self.stock}", f"- {df_pos['Position'][-1]}")            
            return 
    
    
    def macd(self, data):
        data['macd'], data['macdsignal'], data['macdhist'] = ta.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        stock_df = pd.DataFrame(data)

        stock_df["Signal"] = 0.0
        stock_df["Signal"] = np.where(stock_df['macd'] > stock_df['macdsignal'], 1.0, 0.0)
        stock_df["Position"] = stock_df["Signal"].diff()
        df_pos = stock_df[(stock_df["Position"] == 1) | (stock_df["Position"] == -1)]
        df_pos["Position"] = df_pos["Position"].apply(lambda x: "Buy" if x == 1 else "Sell")
        stock_df.dropna(inplace=True)    
        
        if self.graphit is True:
            fig, ax = plt.subplots()
            # plot close price, short-term and long-term moving averages
            plt.tick_params(axis="both", labelsize=15)
            stock_df["macdhist"].plot(color="r", lw=1.5, label="macdhist")
            stock_df['macd'].plot(color="b", lw=2, label='macd')
            stock_df['macdsignal'].plot(color="g", lw=2, label='macdsignal')
            # plot 'buy' signals
            plt.plot(
                stock_df[stock_df["Position"] == 1].index,
                stock_df['macd'][stock_df["Position"] == 1],
                "^", markersize=15, color="g", alpha=0.7, label="buy",
            )
            # plot 'sell' signals
            plt.plot(
                stock_df[stock_df["Position"] == -1].index,
                stock_df['macd'][stock_df["Position"] == -1],
                "v", markersize=15, color="r", alpha=0.7, label="sell",
            )
            plt.ylabel("MACD", fontsize=20, fontweight="bold")
            plt.xlabel("Date", fontsize=20, fontweight="bold")
            plt.title(f"{self.stock} - MACD", fontsize=30, fontweight="bold")
            plt.grid(True, color="k", linestyle="-", linewidth=1, alpha=0.3)
            ax.legend(loc="best", prop={"size": 16})
            plt.tight_layout()
            plt.show()
            st.pyplot(fig)
        
        if df_pos['Position'][-1] == 'Buy':
            st.metric(f"No. {self.cc} / {self.ccc} In Portfolio", f"{self.stock}", f"{df_pos['Position'][-1]}");
            return self.stock
        elif df_pos['Position'][-1] == 'Sell':
            st.metric(f"No. {self.cc} / {self.ccc} In Portfolio", f"{self.stock}", f"- {df_pos['Position'][-1]}")            
            return

        act_lst = []
        for i in stock_df['Position']:
            if i == 1.0:
                act_lst.append('Buy')
            elif i == -1.0:
                act_lst.append('Sell')
            else:
                act_lst.append('')
        stock_df['action'] = act_lst
        del stock_df['Open']
        del stock_df['High']
        del stock_df['Low']
        del stock_df['Adj Close']
        del stock_df['Volume']
        stock_df = stock_df[stock_df['action'] != ""]        
        
         
        
    def rsi(self, data):
        df = pd.DataFrame(data).reset_index()
        df.columns = [x.lower() for x in df.columns]
        df.date = df.date.astype("str")
        date = [datetime.strptime(d, "%Y-%m-%d") for d in df["date"]]
        
        candlesticks = list(
            zip(
                mdates.date2num(date),
                df["open"],
                df["high"],
                df["low"],
                df["close"],
                df["volume"],
            )
        )

        df['rsi'] = ta.RSI(df['close'], timeperiod=14)
        df.dropna(inplace=True)


        def removal(signal, repeat):
            copy_signal = np.copy(signal)
            for j in range(repeat):
                for i in range(3, len(signal)):
                    copy_signal[i - 1] = (copy_signal[i - 2] + copy_signal[i]) / 2
            return copy_signal


        def get(original_signal, removed_signal):
            buffer = []
            for i in range(len(removed_signal)):
                buffer.append(original_signal[i] - removed_signal[i])
            return np.array(buffer)

                
        signal = np.copy(df.open.values)
        removed_signal = removal(signal, 30)
        noise_open = get(signal, removed_signal)

        signal = np.copy(df.high.values)
        removed_signal = removal(signal, 30)
        noise_high = get(signal, removed_signal)

        signal = np.copy(df.low.values)
        removed_signal = removal(signal, 30)
        noise_low = get(signal, removed_signal)

        signal = np.copy(df.close.values)
        removed_signal = removal(signal, 30)
        noise_close = get(signal, removed_signal)

        noise_candlesticks = list(
            zip(mdates.date2num(date), 
            noise_open, 
            noise_high, 
            noise_low, 
            noise_close
            )
        )
        df = df.set_index('date')
        
        if self.graphit is True:
            fig, ax = plt.subplots()
            # plot close price, short-term and long-term moving averages
            plt.tick_params(axis="both", labelsize=15)
            df.loc["2021":, "rsi"].plot(color="k", lw=2, label="rsi")
            ax.plot(
                df.index,
                [np.percentile(noise_close, 95)] * len(noise_candlesticks),
                color=(1.0, 0.792156862745098, 0.8, 1.0),
                linewidth=5.0,
                label="overbought line",
                alpha=1.0,
            )
            ax.plot(
                df.index,
                [np.percentile(noise_close, 82)] * len(noise_candlesticks),
                color=(0.6627450980392157, 1.0, 0.6392156862745098, 1.0),
                linewidth=5.0,
                label="oversold line",
                alpha=1.0,
            )
            plt.ylabel("RSI", fontsize=20, fontweight="bold")
            plt.xlabel("Date", fontsize=20, fontweight="bold")
            plt.title(f"{self.stock} - RSI", fontsize=30, fontweight="bold")
            plt.grid(True, color="k", linestyle="-", linewidth=1, alpha=0.3)
            ax.legend(loc="best", prop={"size": 16})
            plt.tight_layout()
            plt.show()
            st.pyplot(fig)

        df["Signal"] = 0.0
        df["Signal"] = np.where(df['rsi'] > 30, 1.0, 0.0)
        df["Position"] = df["Signal"].diff()        
        df_pos = df[(df["Position"] == 1) | (df["Position"] == -1)]
        df_pos["Position"] = df_pos["Position"].apply(lambda x: "Buy" if x == 1 else "Sell")   
        
        if df_pos['Position'][-1] == 'Buy':
            st.metric(f"No. {self.cc} / {self.ccc} In Portfolio", f"{self.stock}", f"{df_pos['Position'][-1]}");
            return self.stock
        elif df_pos['Position'][-1] == 'Sell':
            st.metric(f"No. {self.cc} / {self.ccc} In Portfolio", f"{self.stock}", f"- {df_pos['Position'][-1]}")            
            return
        
        
    def kingpin(self, mod):                
        data = self.get_data()
        
        if mod == 'Bollinger Bands':      
            ret = self.bollinger_bands(self.data)
            if ret == self.stock:
                return self.stock
            else:
                return 
            
        elif mod == 'MACD':      
            ret = self.macd(self.data)
            if ret == self.stock:
                return self.stock
            else:
                return 
        
        elif mod == 'RSI':      
            ret = self.rsi(self.data)
            if ret == self.stock:
                return self.stock
            else:
                return 