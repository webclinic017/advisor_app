import warnings
warnings.filterwarnings("ignore")
from datetime import timedelta, datetime, date
import matplotlib as mpl
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st
from scipy.stats import norm

import src.tools.functions as f0

warnings.filterwarnings("ignore")
mpl.use("Agg")
plt.style.use("ggplot")
sm, med, lg = 10, 15, 20
plt.rc("font", size=sm)                     # controls default text sizes
plt.rc("axes", titlesize=med)               # fontsize of the axes title
plt.rc("axes", labelsize=med)               # fontsize of the x & y labels
plt.rc("xtick", labelsize=sm)               # fontsize of the tick labels
plt.rc("ytick", labelsize=sm)               # fontsize of the tick labels
plt.rc("legend", fontsize=sm)               # legend fontsize
plt.rc("figure", titlesize=lg)              # fontsize of the figure title
plt.rc("axes", linewidth=2)                 # linewidth of plot lines
plt.rcParams["figure.figsize"] = [15, 7]
plt.rcParams["figure.dpi"] = 134



class The_Monte_Carlo(object):
    
    def __init__(self, stock):
        self.stock = stock
        self.company = f0.company_longName(self.stock)


    def creation_A(self, hist="5y"):
        stock_data = yf.Ticker(self.stock)
        df = stock_data.history(hist, auto_adjust=True)

        # - Calculate daily returns:
        adj_close = df["Close"]
        returns = adj_close.pct_change().dropna()
        
        # - Split data into the training and test sets:
        train = returns[:"2021-01-01"]
        test = returns["2021-01-01":]

        # - Specify the parameters of the simulation:
        dt = 1
        T = 150
        N_SIM = 100
        N = len(test)
        S_0 = adj_close[train.index[-1]]
        mu = train.mean()
        sigma = train.std()
        
        
        # t_intervals = 200
        # iterations = 100       
         
        # log_returns = np.log(1 + data.pct_change())
        # u = log_returns.mean()
        # var = log_returns.var()
        # drift = u - (0.5 * var)
        # stdev = log_returns.std()
        # norm.ppf(0.95)
        # x = np.random.rand(10, 2)
        # norm.ppf(x)
        # Z = norm.ppf(np.random.rand(10,2))
        # S0 = data.iloc[-1]  

        
        def simulate_gbm(s_0, mu, sigma, n_sims, dt, T, N, random_seed=42):
            """
            Function used for simulating stock returns using Geometric Brownian Motion.
            Parameters ------------
            s_0 : float - Initial stock price
            mu : float - Drift coefficient
            sigma : float - Diffusion coefficient
            n_sims : int - Number of simulations paths
            dt : float - Time increment, most commonly a day
            T : float - Length of the forecast horizon, same unit as dt
            N : int - Number of time increments in the forecast horizon
            random_seed : int - Random seed for reproducibility
            Returns ----------- S_t : np.ndarray
                Matrix (size: n_sims x (T+1)) containing the simulation results.
                Rows respresent sample paths, while columns point of time.
            """
            np.random.seed(random_seed)
            dt = T / N
            dW = np.random.normal(scale=np.sqrt(dt), size=(n_sims, N))
            W = np.cumsum(dW, axis=1)

            time_step = np.linspace(dt, T, N)
            time_steps = np.broadcast_to(time_step, (n_sims, N))

            S_t = s_0 * np.exp((mu - 0.5 * sigma ** 2) * time_steps + sigma * W)
            S_t = np.insert(S_t, 0, s_0, axis=1)
            return S_t

        gbm_simulations = simulate_gbm(S_0, mu, sigma, N_SIM, dt, T, N)
        
        # create sim date results
        last_train_date = train.index[-1].date()
        
        # first_test_date = test.index[0].date()
        last_test_date = test.index[-1].date()
        selected_indices = adj_close[last_train_date:last_test_date].index
        index = [date.date() for date in selected_indices]
        gbm_simulations_df = pd.DataFrame(np.transpose(gbm_simulations), index=index)

        # plotting
        fig, ax = plt.subplots()
        ax = gbm_simulations_df.plot(alpha=0.2, legend=False)
        (line_1,) = ax.plot(index, gbm_simulations_df.mean(axis=1), color="red")
        (line_2,) = ax.plot(index, adj_close[last_train_date:last_test_date], color="blue")
        ax.set_title(f"{self.company} - ({self.stock}) - Monte Carlo Simulations", fontsize=30, fontweight="bold")
        ax.legend((line_1, line_2), ("mean-price", "actual-price"))
        plt.xlabel("Test Date Range", fontsize=20, fontweight="bold")
        plt.ylabel("Stock Price", fontsize=20, fontweight="bold")
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(15)
        ax.grid(True, color="k", linestyle="-", linewidth=1, alpha=0.3)
        plt.tight_layout()
        st.pyplot(plt.show())
        plt.close(fig)



    def creation_B(self):
        data = pd.DataFrame(yf.download(self.stock, start='2012-01-03', end='2022-01-03')['Adj Close'])
        data.columns = [self.stock]
        pred_date = data.index[-1]        
        
        log_returns = np.log(1 + data.pct_change())
        u = log_returns.mean()
        var = log_returns.var()
        drift = u - (0.5 * var)
        stdev = log_returns.std()
        norm.ppf(0.95)
        x = np.random.rand(10, 2)
        norm.ppf(x)
        Z = norm.ppf(np.random.rand(10, 2))
        S0 = data.iloc[-1]        
        t_intervals = 252
        iterations = 250
        metric1 = (t_intervals-1)
        
        daily_returns = np.exp(drift.values + stdev.values * norm.ppf(np.random.rand(t_intervals, iterations)))
        
        price_list = np.zeros_like(daily_returns)
        price_list[0] = S0
        for t in range(1, t_intervals):
            price_list[t] = price_list[t - 1] * daily_returns[t]
            
        today = datetime(2022, 1, 1)
        days_lst = [today]
        for i in range(metric1):
            tday = days_lst[-1]
            next = tday + timedelta(days=1)
            days_lst.append(next)   
        
        price_list_df = pd.DataFrame.from_records(price_list)
        price_list_df['date'] = days_lst
        price_list_df = price_list_df.set_index('date')
        price_list_df.index = pd.to_datetime(price_list_df.index)
        
        new_df = yf.download(self.stock, start=str(pred_date)[:10]).iloc[:metric1+1]
        selected_indices = new_df.index
        index = [date.date() for date in selected_indices]            
        
        company_name = f0.company_longName(self.stock)
        x = f"{company_name} - [{self.stock}]"
        st.header(f"𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄚𝄚 {x} 𝄚𝄚𝄙𝄙𝄘𝄘𝄗𝄗𝄖𝄖")
        st.subheader("𝄖𝄗𝄘𝄙𝄚 Metrics:")
        st.write(f"- Forecast Intervals (days): {t_intervals}")
        st.write(f"- Simulation Iterations {iterations}")
        
        fig, ax = plt.subplots()
        ax = price_list_df.plot(label=price_list_df.columns, lw=1.5, ls='--', alpha=0.8, legend=False)
        (line_1,) = ax.plot(price_list_df.index, price_list_df.mean(axis=1), color="red", lw=3)
        (line_2,) = ax.plot(new_df.index, new_df['Adj Close'], color="blue", lw=3)
        (line_3) = plt.axvline(x=datetime.now(), color='k', linestyle='--')
        ax.legend((line_1, line_2, line_3), ("mean-projection", "actual-history", "today"))
        plt.xlabel('Date', fontsize=20, fontweight="bold")
        plt.ylabel('Price', fontsize=20, fontweight="bold")
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(15)
        ax.grid(True, alpha=0.3)        
        plt.tight_layout()
        st.pyplot(plt.show())
        plt.close(fig)