import warnings
import streamlit as st
from fbprophet.plot import add_changepoints_to_plot
from fbprophet import Prophet
import yfinance as yf
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from finvizfinance.quote import finvizfinance

from src.tools import functions as f2
from yahoo_fin import stock_info as si

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


score = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
rating = ["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell", "No Data"]
scale = dict(zip(rating, score))


def get_key(val):
    for key, value in scale.items():
        if val == value:
            return key


class Web_prophet_kyle(object):
    def __init__(self, stock, per=360, hist="5y"):
        """
        forecast the given ticker (stock) period days into the future (from today)
        ---------inputs----------
        > ticker ->> ticker of stock to forecast
        > periods->> number of days into the future to forecast (from today's date)
        > hist   ->> amount of historical data to use
            [default=max] -> options(1d,5d,1mo,3mo,6mo,1y,2y,5y,10y}
        """
        self.stock = stock
        self.per = per
        self.hist = hist
        self.company = f2.company_longName(self.stock)

    def run_prophet(self):
        import pathlib

        file = pathlib.Path(f"data/raw/2021-09-01/{self.stock}.pkl")
        if file.exists():
            df = pd.read_pickle(f"data/raw/2021-09-01/{self.stock}.pkl")
        else:
            stock_data = yf.Ticker(self.stock)
            df = stock_data.history(self.hist, auto_adjust=True)

        df.reset_index(inplace=True)
        df.fillna(0.0, inplace=True)
        df = df[["Date", "Close"]]  # select Date and Price
        df = df.rename(columns={"Date": "ds", "Close": "y"})

        # create a Prophet model from that data
        m = Prophet(
            daily_seasonality=True,
            changepoint_prior_scale=0.1,
            seasonality_prior_scale=10,
            stan_backend=None,
        )

        m.fit(df)
        future = m.make_future_dataframe(self.per, freq="D")
        forecast = m.predict(future)
        forecast = forecast[["ds", "trend", "yhat_lower", "yhat_upper", "yhat"]]

        # create plot
        fig1 = m.plot(
            forecast,
            ax=None,
            uncertainty=True,
            plot_cap=True,
            xlabel="Date",
            ylabel="Stock Price",
        )

        add_changepoints_to_plot(fig1.gca(), m, forecast)
        plt.title(
            f"Prophet Model ChangePoints - {self.company} ({self.stock}) - {self.per} Day Forecast"
        )
        plt.legend(["actual", "prediction", "changePoint_line"], loc="best")
        st.pyplot(fig1)

        try:
            fd = yf.download(self.stock, period="1d")
            x = round(float(fd["Adj Close"]), 2)
            st.subheader(
                f" > {self.company} · [{self.stock}] - Current Stock Price = **${x}**"
            )
        except Exception:
            pass

        try:
            st.subheader(
                f" > {self.company} · [{self.stock}] - {self.per} · Day Forcast Price = ** ${round(float(forecast['yhat'].iloc[-1]),2)} **"
            )
        except Exception:
            pass

        try:
            analyst_1yr = float(
                finvizfinance(self.stock).TickerFundament()["Target Price"]
            )
            st.subheader(
                f" > {self.company} · [{self.stock}] - Current Analyst 1yr Price Estimate = **{analyst_1yr}**"
            )
        except Exception:
            pass

        return


if __name__ == "__main__":
    Web_prophet_kyle("NVDA").run_prophet()
