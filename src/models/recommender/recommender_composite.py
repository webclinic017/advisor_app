import warnings
from finvizfinance.quote import finvizfinance
import yfinance as yf
from yahooquery import Ticker
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from os.path import exists

from src.data.source_data import Source_Data
import src.data.yahoo_fin_stock_info as si

warnings.filterwarnings("ignore")
pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.width = None
pd.options.display.float_format = "{:,}".format
nltk.download("vader_lexicon")

today_stamp = str(datetime.now())[:10]
saveRaw = Path(f"data/raw/{today_stamp}/")
# saveRec_01 = Path(f"data/recommenders/{today_stamp}/rec_01/")


if not saveRaw.exists():
    saveRaw.mkdir(parents=True)

# if not saveRec_01.exists():
#     saveRec_01.mkdir(parents=True)

saveRec = Path(f"data/recommenders/{today_stamp}/")
if not saveRec.exists():
    saveRec.mkdir(parents=True)


def company_longName(symbol):
    d = Ticker(symbol).quote_type
    return list(d.values())[0]["longName"]


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#      *       *       *       *                                                   > model: [ RECOMMENDER_STAGE_01 ]


class Recommendations1(object):
    def __init__(self, ticker_list):
        self.ticker_list = ticker_list
        self.recommendations = []

    def run_rec1(self):
        for s in self.ticker_list:
            try:
                recommendation = finvizfinance(s).TickerFundament()["Recom"]
            except Exception:
                recommendation = 6.0
            if recommendation == "-":
                recommendation = 6.0
            self.recommendations.append(round(float(recommendation), 2))

        dataframe = (
            pd.DataFrame(
                list(zip(self.ticker_list, self.recommendations)),
                columns=["Company", "Recommendations"],
            )
            .sort_values("Recommendations")
            .set_index("Company")
        )

        dataframe.to_pickle(saveRec / "recommender_00_return_dataFrame.pkl")

        dataframe_02 = dataframe[dataframe["Recommendations"] < 2.6]
        dataframe_02.columns = ["Symbol", "Score"]
        dataframe_02["rank"] = range(1, len(dataframe_02["Symbol"]) + 1)
        dataframe_02.set_index("rank").to_pickle(
            saveRec / "recommender_01_return_dataFrame.pkl"
        )

        return


#     *       *       *       *                                                   > model: [ RECOMMENDER_STAGE_02 ]


class Recommendations2(object):
    # Variables
    def __init__(self, tickers):
        self.tickers = tickers
        self.sName = "Recommender 02 Return List"
        self.index_name = "^GSPC"  # S&P 500
        self.start_date = datetime.now() - timedelta(days=365)
        self.end_date = date.today()

    def run_rec2(self):
        returns_multiples = []
        exportList = pd.DataFrame(
            columns=[
                "Symbol",
                "Company",
                "RS_Rating",
                "Returns_multiple",
                "currentClose",
                "20 Day MA",
                "50 Day Ma",
                "200 Day MA",
                "52 Week Low",
                "52 week High",
            ]
        )

        # Index Returns
        index_df = yf.download(self.index_name, period="1y")
        index_df["Percent Change"] = index_df["Adj Close"].pct_change()
        index_return = (index_df["Percent Change"] + 1).cumprod()[-1]

        # Find top 30% performing Tickers (relative to the S&P 500)
        c0 = 0
        for ticker in self.tickers:
            c0 += 1
            try:
                df = yf.download(ticker, period="1y")
                df.to_pickle(saveRaw / f"{ticker}.pkl")
            except Exception:
                pass

            # Calculating returns relative to the market (returns multiple)
            try:
                df["Percent Change"] = df["Adj Close"].pct_change()
                stock_return = (df["Percent Change"] + 1).cumprod()[-1]
                returns_multiple = round((stock_return / index_return), 2)
                returns_multiples.extend([returns_multiple])
                st.write(
                    f"{c0}) Ticker: {ticker}; Returns Multiple against S&P 500: {returns_multiple}\n"
                )
            except Exception:
                pass

        # Creating dataframe of only top 30%
        rs_df = pd.DataFrame(
            list(zip(self.tickers, returns_multiples)),
            columns=["Symbol", "Returns_multiple"],
        )
        rs_df["RS_Rating"] = rs_df.Returns_multiple.rank(pct=True) * 100
        rs_df = rs_df[rs_df.RS_Rating >= rs_df.RS_Rating.quantile(0.65)]

        # Checking Minervini conditions of top 30% of stocks in given list
        rs_stocks = rs_df["Symbol"]
        for stock in rs_stocks:
            try:
                df = pd.read_pickle(saveRaw / f"{stock}.pkl", index_col=0)
                sma = [20, 50, 200]
                for x in sma:
                    df["SMA_" + str(x)] = round(
                        df["Adj Close"].rolling(window=x).mean(), 2
                    )

                # Storing required values
                currentClose = df["Adj Close"][-1]
                moving_average_20 = df["SMA_20"][-1]
                moving_average_50 = df["SMA_50"][-1]
                moving_average_200 = df["SMA_200"][-1]
                low_of_52week = round(min(df["Low"][-260:]), 2)
                high_of_52week = round(max(df["High"][-260:]), 2)
                RS_Rating = round(rs_df[rs_df["Symbol"] == stock].RS_Rating.tolist()[0])
                Returns_multiple = rs_df[
                    rs_df["Symbol"] == stock
                ].Returns_multiple.tolist()[0]
                try:
                    moving_average_200_20 = df["SMA_200"][-20]
                except Exception:
                    moving_average_200_20 = 0

                # Condition 1: Current Price > 50 SMA and > 200 SMA
                condition_1 = currentClose > moving_average_50 > moving_average_200
                # Condition 2: 50 SMA and > 200 SMA
                condition_2 = moving_average_50 > moving_average_200
                # Condition 3: 200 SMA trending up for at least 1 month
                condition_3 = moving_average_200 > moving_average_200_20
                # Condition 4: 50 SMA>50 SMA and 50 SMA> 200 SMA
                condition_4 = moving_average_20 > moving_average_50 > moving_average_200
                # Condition 5: Current Price > 50 SMA
                condition_5 = currentClose > moving_average_50
                # Condition 6: Current Price is at least 10% above 52 week low
                condition_6 = currentClose >= (1.1 * low_of_52week)
                # Condition 7: Current Price is within 50% of 52 week high
                condition_7 = currentClose >= (0.50 * high_of_52week)
                # If all conditions above are true, add Ticker to exportList

                if (
                    condition_1
                    & condition_2
                    & condition_3
                    & condition_4
                    & condition_5
                    & condition_6
                    & condition_7
                ):
                    exportList = exportList.append(
                        {
                            "Symbol": stock,
                            "Company": company_longName(stock),
                            "RS_Rating": RS_Rating,
                            "Returns_multiple": Returns_multiple,
                            "currentClose": currentClose,
                            "20 Day MA": moving_average_20,
                            "50 Day Ma": moving_average_50,
                            "200 Day MA": moving_average_200,
                            "52 Week Low": low_of_52week,
                            "52 week High": high_of_52week,
                        },
                        ignore_index=True,
                    ).sort_values(by="RS_Rating", ascending=False)

            except Exception as e:
                print(e)
                print(f"Could not gather data on {stock}")
        exportList = exportList.drop_duplicates(subset="Symbol")
        exportList["rank"] = range(1, len(exportList["Symbol"]) + 1)
        exportList = exportList.set_index("rank")
        exportList.to_pickle(saveRec / "recommender_02_return_dataFrame.pkl")
        return


if __name__ == "__main__":
    ticker_lst = pd.read_pickle(saveRec / "recommender_01_return_dataFrame.pkl")["Symbol"]
    Recommendations2(ticker_lst).run_rec2()


#       *       *       *                                                  > model: [ RECOMMENDER_STAGE_03 ]


import warnings
from finvizfinance.quote import finvizfinance
import yfinance as yf
from yahooquery import Ticker
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from pathlib import Path
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import finviz

from src.data.source_data import Source_Data
import src.data.yahoo_fin_stock_info as si

warnings.filterwarnings("ignore")
pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.width = None
pd.options.display.float_format = "{:,}".format
nltk.download("vader_lexicon")

today_stamp = str(datetime.now())[:10]
# today_stamp = '2021-09-06'
saveRaw = Path(f"data/raw/{today_stamp}/")
# saveRec_01 = Path(f"data/recommenders/{today_stamp}/rec_01/")


if not saveRaw.exists():
    saveRaw.mkdir(parents=True)

# if not saveRec_01.exists():
#     saveRec_01.mkdir(parents=True)

saveRec = Path(f"data/recommenders/{today_stamp}/")
if not saveRec.exists():
    saveRec.mkdir(parents=True)


def company_longName(symbol):
    d = Ticker(symbol).quote_type
    return list(d.values())[0]["longName"]


class Recommendations3(object):
    # Parameters
    def __init__(self, symbols):
        print(f"\n - - - Starting Ticker List Length = {len(symbols)} - - -\n")
        for s in symbols:
            try:
                finviz.get_news(s)
            except:
                print(f" - {s}")
                symbols.remove(s)

        self.n = 3
        self.tickers = symbols
        print(f"\n - - - Resulting Ticker List Length = {len(self.tickers)} - - -\n")

    # Get Data
    def recommender_3_1(self):
        finwiz_url = "https://finviz.com/quote.ashx?t="
        news_tables = {}

        for ticker in self.tickers:
            url = finwiz_url + ticker
            req = Request(url=url, headers={"user-agent": "my-app/0.0.1"})
            resp = urlopen(req)
            html = BeautifulSoup(resp, features="lxml")
            news_table = html.find(id="news-table")
            news_tables[ticker] = news_table

        remove_pile = []
        for ticker in self.tickers:
            df = news_tables[ticker]
            if df:
                try:
                    df_tr = df.findAll("tr")
                    st.subheader("Recent News Headlines for [{}]: ".format(ticker))
                    for i, table_row in enumerate(df_tr):
                        a_text = table_row.a.text
                        td_text = table_row.td.text
                        td_text = td_text.strip()
                        st.write("* ", a_text, "(", td_text, ")")
                        if i == self.n - 1:
                            break
                except:
                    remove_pile.append(ticker)
                    print(ticker)
                    pass

        if remove_pile:
            for r in remove_pile:
                self.tickers.remove(r)

        # Iterate through the news
        parsed_news = []
        for file_name, news_table in news_tables.items():
            for x in news_table.findAll("tr"):
                text = x.a.get_text()
                date_scrape = x.td.text.split()
                if len(date_scrape) == 1:
                    time = date_scrape[0]
                else:
                    date = date_scrape[0]
                    time = date_scrape[1]
                ticker = file_name.split("_")[0]
                parsed_news.append([ticker, date, time, text])

        # Sentiment Analysis
        analyzer = SentimentIntensityAnalyzer()
        columns = ["Symbol", "Date", "Time", "Headline"]
        news = pd.DataFrame(parsed_news, columns=columns)
        scores = news["Headline"].apply(analyzer.polarity_scores).tolist()
        df_scores = pd.DataFrame(scores)
        news = news.join(df_scores, rsuffix="_right")

        # View Data
        news["Date"] = pd.to_datetime(news.Date).dt.date
        unique_ticker = news["Symbol"].unique().tolist()
        news_dict = {name: news.loc[news["Symbol"] == name] for name in unique_ticker}
        values = []
        for ticker in self.tickers:
            dataframe = news_dict[ticker]
            dataframe = dataframe.set_index("Symbol")
            dataframe = dataframe.drop(columns=["Headline"])
            mean = round(dataframe["compound"].mean() * 100, 0)
            values.append(mean)

        df = pd.DataFrame(self.tickers, columns=["Symbol"])

        company_lst_0 = list(df["Symbol"])
        company_lst_1 = []
        [company_lst_1.append(company_longName(x)) for x in company_lst_0]

        df["company_name"] = company_lst_1
        df["Mean Sentiment"] = values
        df = df.sort_values("Mean Sentiment", ascending=False)
        df["rank"] = range(1, len(df.index) + 1)
        df = df.set_index("rank")
        df_03 = df[df["Mean Sentiment"] >= 10]
        df_03.to_pickle(saveRec / "recommender_03_return_dataFrame.pkl")
        return


if __name__ == "__main__":
    ticker_lst = list(
        pd.read_pickle(saveRec / "recommender_02_return_dataFrame.pkl")["Symbol"]
    )

    for s in ticker_lst:
        lst = list(s)
        if len(lst) > 4:
            if lst[-1] == "F" or lst[-1] == "Y":
                ticker_lst.remove(s)

    Recommendations3(ticker_lst).recommender_3_1()


#       *       *       *       *                                         > model: [ RECOMMENDER_STAGE_04 ]


class Recommendations4(object):
    def __init__(self, stock_ticker):
        self.stock_ticker = stock_ticker

    def recommender_4_1(self):
        yfTicker = yf.Ticker(self.stock_ticker)
        recommendation = yfTicker.recommendations
        new = []
        date = []
        for r in recommendation.index:
            date.append(r)
            new.append(str(r)[:10])
        recommendation.index = new
        recommendation["date"] = date
        year = []
        for r in recommendation.index:
            year.append(int(r[:4]))
        recommendation["year"] = year
        recommendation[recommendation["year"] > 2019]
        recommendation.sort_values("date", ascending=False, inplace=True)
        self.recommendation = recommendation
        return self.recommendation.head(10)

    def recommender_4_2(self):
        grade_set1 = set(self.recommendation["To Grade"])
        grade_list = list(self.recommendation["To Grade"])
        grade_set = []
        for g in grade_set1:
            if g != "":
                grade_set.append(g)
        counts = []
        for s in grade_set:
            counts.append(grade_list.count(s))

        fd = pd.DataFrame()
        fd["grade"] = grade_set
        fd["counts"] = counts
        fd.set_index("grade", inplace=True)
        fd = fd.sort_values("counts", ascending=False)

        st.header(f"** {company_longName(self.stock_ticker)} [{self.stock_ticker}]**")
        st.write(
            f"** · Visualize All Current Analyst Recommendations [{self.stock_ticker}]**"
        )

        fig, ax = plt.subplots()
        ax.bar(fd.index, fd["counts"])
        plt.xticks(rotation=80)
        st.pyplot(fig)

        new_df = pd.DataFrame(fd[:5])
        tot_count = new_df.counts.sum()
        new_df["Percent_of_Total"] = round(((new_df["counts"] / tot_count) * 100), 2)
        labels = list(new_df.index)
        sizes = list(new_df["Percent_of_Total"])
        explode_0 = [0.1]
        # (0.1, 0.0, 0, 0) - only "explode" the 2nd slice (i.e. 'Hogs')
        [explode_0.append(0.0) for x in range(1, len(new_df.index))]
        explode = tuple(explode_0)

        st.write(f"** · Top 5 Analyst Recommendations [{self.stock_ticker}]**")

        fig1, ax1 = plt.subplots()
        ax1.pie(
            sizes,
            labels=labels,
            explode=explode,
            autopct="%1.1f%%",
            shadow=True,
            startangle=90,
        )
        ax1.axis("equal")
        # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig1)
        st.write("** · Total Analyst Ratings · **")
        st.dataframe(fd)
        st.write("__" * 25)
        return fd


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

if __name__ == "__main__":
    # stock_ticker_list = si.tickers_dow()
    # title_a = "DOW JONES STOCK TICKERS"
    # for s in stock_ticker_list[:5]:
    #     stage = Recommendations4(s)
    #     stage.recommender_4_1()

    file_loc = Path(f"data/recommenders/2021-08-13/recommender_04_return_dataFrame.pkl")
