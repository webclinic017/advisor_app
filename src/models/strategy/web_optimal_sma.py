from PIL.Image import ROTATE_90
import yfinance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from datetime import datetime, date
from yahooquery import Ticker
import streamlit as st

plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = [10, 7]
plt.rc("font", size=14)
np.random.seed(0)


class Optimal_SMA(object):
    def __init__(self, ticker):
        self.name = ticker
        self.n_forward = 1
        self.start_date = "2010-01-01"
        self.end_date = datetime.now()

        def company_longName(symbol):
            d = Ticker(symbol).quote_type
            return list(d.values())[0]["longName"]

        self.company_longName = company_longName(self.name)

        self.ticker = yfinance.Ticker(self.name)
        self.data = self.ticker.history(period="max", interval="1d")

    def build_optimal_sma(self):
        fig, ax = plt.subplots()
        plt.plot(self.data["Close"], label=self.company_longName)
        plt.plot(self.data["Close"].rolling(20).mean(), label="20-periods SMA")
        plt.plot(self.data["Close"].rolling(50).mean(), label="50-periods SMA")
        plt.plot(self.data["Close"].rolling(200).mean(), label="200-periods SMA")
        plt.xlabel("Date", fontsize=20, fontweight="bold")
        plt.ylabel("Price", fontsize=20, fontweight="bold")
        plt.title(
            f"{self.company_longName} ({self.name}) - SMA",
            fontsize=30,
            fontweight="bold",
        )
        plt.xlim((date(2020, 1, 1)), (date(2021, 6, 1)))
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(15)
        ax.grid(True, color="k", linestyle="-", linewidth=1, alpha=0.3)
        plt.xticks(rotation=45)
        plt.yticks(rotation=90)
        ax.legend(loc="best", prop={"size": 16})
        plt.tight_layout()
        st.pyplot(fig)

        self.data["Forward Close"] = self.data["Close"].shift(-self.n_forward)
        self.data["Forward Return"] = (
            self.data["Forward Close"] - self.data["Close"]
        ) / self.data["Close"]

        result = []
        train_size = 0.6

        for sma_length in range(20, 500):
            self.data["SMA"] = self.data["Close"].rolling(sma_length).mean()
            self.data["input"] = [int(x) for x in self.data["Close"] > self.data["SMA"]]
            df = self.data.dropna()

            training = df.head(int(train_size * df.shape[0]))
            test = df.tail(int((1 - train_size) * df.shape[0]))
            tr_returns = training[training["input"] == 1]["Forward Return"]
            test_returns = test[test["input"] == 1]["Forward Return"]

            mean_forward_return_training = tr_returns.mean()
            mean_forward_return_test = test_returns.mean()
            pvalue = ttest_ind(tr_returns, test_returns, equal_var=False)[1]

            result.append(
                {
                    "sma_length": sma_length,
                    "training_forward_return": mean_forward_return_training,
                    "test_forward_return": mean_forward_return_test,
                    "p-value": pvalue,
                }
            )
        result.sort(key=lambda x: -x["training_forward_return"])
        fd = pd.DataFrame(result)
        fd.set_index("sma_length", inplace=True)

        best_sma = result[0]["sma_length"]
        self.data["SMA"] = self.data["Close"].rolling(best_sma).mean()

        fig, ax = plt.subplots()
        plt.plot(self.data["Close"], label=self.company_longName)
        plt.plot(self.data["SMA"], label="{} periods SMA".format(best_sma))
        plt.xlabel("Date", fontsize=20, fontweight="bold")
        plt.ylabel("Price", fontsize=20, fontweight="bold")
        plt.title(
            f"{self.company_longName} ({self.name}) - SMA",
            fontsize=30,
            fontweight="bold",
        )
        plt.xlim((date(2020, 1, 1)), (date(2021, 6, 1)))
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(15)
        ax.grid(True, color="k", linestyle="-", linewidth=1, alpha=0.3)
        plt.xticks(rotation=45)
        plt.yticks(rotation=90)
        ax.legend(loc="best", prop={"size": 16})
        plt.tight_layout()
        st.pyplot(fig)

        st.write(
            f"* {self.company_longName} ({self.name}) - Best Single SMA  = [{best_sma}]"
        )

        return best_sma


if __name__ == "__main__":
    Optimal_SMA("NVDA").build_optimal_sma()
