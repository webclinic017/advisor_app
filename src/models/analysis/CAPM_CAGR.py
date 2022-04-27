from pandas.core.indexes import period
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime
import streamlit as st

import src.tools.functions as f0


class CAPM_CAGR(object):
    
    
    def __init__(self):
        st.subheader("𝄖𝄗𝄗𝄘𝄘𝄘𝄙𝄙𝄙𝄙 Ratio · Analysis [CAPM & CAGR] 𝄙𝄙𝄙𝄙𝄘𝄘𝄘𝄗𝄗𝄖")


    def import_stock_data(self, tickers, start="2010-1-1", end=datetime.today().strftime("%Y-%m-%d")):
        data = pd.DataFrame(yf.download(tickers, period="1y")["Adj Close"])
        return data


    def compute_beta(self, data, stock, market):
        log_returns = np.log(data / data.shift(1))
        cov = log_returns.cov() * 250
        cov_w_market = cov.loc[stock, market]
        market_var = log_returns[market].var() * 250
        return cov_w_market / market_var


    def CAGR(self, data):
        df = data.copy()
        df["daily_returns"] = df["Adj Close"].pct_change()
        df["cumulative_returns"] = (1 + df["daily_returns"]).cumprod()
        trading_days = 252
        n = len(df) / trading_days
        cagr = (df["cumulative_returns"][-1]) ** (1 / n) - 1
        return cagr


    def volatility(self, data):
        df = data.copy()
        df["daily_returns"] = df["Adj Close"].pct_change()
        trading_days = 252
        vol = df["daily_returns"].std() * np.sqrt(trading_days)
        return vol


    def compute_capm(self, data, stock, market, riskfree=0.0285):
        log_returns = np.log(data / data.shift(1))
        riskpremium = (log_returns[market].mean() * 252) - riskfree
        beta = self.compute_beta(data, stock, market)
        return riskfree + (beta * riskpremium)


    def sharpe_ratio(self, data, rf):
        df = data.copy()
        sharpe = (self.CAGR(df) - rf) / self.volatility(df)
        return sharpe


    def compute_sharpe(self, data, stock, market, riskfree=0.0285):
        log_returns = np.log(data / data.shift(1))
        ret = self.compute_capm(data, stock, market, riskfree)
        return (ret - riskfree) / (log_returns[stock].std() * 250 ** 0.5)


    def sortino_ratio(self, data, rf):
        df = data.copy()
        df["daily_returns"] = df["Adj Close"].pct_change()
        df["negative_returns"] = np.where(df["daily_returns"] < 0, df["daily_returns"], 0)
        negative_volatility = df["negative_returns"].std() * np.sqrt(252)
        sortino = (self.CAGR(df) - rf) / negative_volatility
        return sortino


    def maximum_drawdown(self, data):
        df = data.copy()
        df["daily_returns"] = df["Adj Close"].pct_change()
        df["cumulative_returns"] = (1 + df["daily_returns"]).cumprod()
        df["cumulative_max"] = df["cumulative_returns"].cummax()
        df["drawdown"] = df["cumulative_max"] - df["cumulative_returns"]
        df["drawdown_pct"] = df["drawdown"] / df["cumulative_max"]
        max_dd = df["drawdown_pct"].max()
        return max_dd


    def calmar_ratio(self, data, rf):
        df = data.copy()
        calmar = (self.CAGR(df) - rf) / self.maximum_drawdown(data)
        return calmar


    def stock_CAPM(self, stock_ticker, market_ticker, start_date="2010-1-1", riskfree=0.025):
        data = self.import_stock_data([stock_ticker, market_ticker], start=start_date)
        beta = self.compute_beta(data, stock_ticker, market_ticker)
        capm = self.compute_capm(data, stock_ticker, market_ticker, riskfree)
        sharpe = self.compute_sharpe(data, stock_ticker, market_ticker, riskfree)
        listcapm = [beta, capm, sharpe]
        return listcapm
    

    def configure_mod(self, ticker_lst):
        df = pd.DataFrame()
        stocks = []
        company_names = []
        betas = []
        returns = []
        sharpes = []
        cagrs = []
        annual_vols = []
        sharpes2 = []
        sortinos = []
        calmars = []
        
        stocks, company_names, betas, returns, sharpes, cagrs, annual_vols, sharpes2, sortinos, calmars = [], [], [], [], [], [], [], [], [], []

        for t in ticker_lst:
            x = self.stock_CAPM(t, "^GSPC")
            stock_data = yf.download(t, period="max")
            
            stocks.append(t)
            company_names.append(f0.company_longName(t))
            betas.append(round(float(x[0]), 4))
            returns.append(round(float(x[1]) * 100, 4))
            sharpes.append(round(float(x[2]), 4))
            cagrs.append(round(self.CAGR(stock_data) * 100, 2))
            annual_vols.append(round(self.volatility(stock_data) * 100, 2))
            sharpes2.append(round(self.sharpe_ratio(stock_data, 0.03), 4))
            sortinos.append(round(self.sortino_ratio(stock_data, 0.03), 4))
            calmars.append(round(self.calmar_ratio(stock_data, 0.03), 4))

        df['Company'] = company_names
        df["Ticker"] = stocks
        df["CAGR"] = cagrs
        df["CAPM"] = returns
        df["Annual Volatility"] = annual_vols        
        df["Beta"] = betas
        df["Sharpe"] = sharpes
        df["Sharpe2"] = sharpes2
        df["Sortino"] = sortinos
        df["Calmar"] = calmars
        df = df.set_index(['Company', 'Ticker'])
        st.table(df)
