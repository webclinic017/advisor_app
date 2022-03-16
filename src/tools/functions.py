import pandas as pd
import yfinance as yf
from yahooquery import Ticker
import streamlit as st
import webbrowser
from datetime import date, timedelta, datetime
from pathlib import Path

# import src.models.portfolio as p1


def recommended_stocks():
    sdate = date(2021, 7, 15)  # start date
    edate = datetime.now()
    report_date = st.sidebar.date_input(
        label="> recommender date:",
        value=date(2021, 7, 15),
        min_value=sdate,
        max_value=edate,
        key="date to run proof",
        help="Select a date in the range between 2021.07.15 - 2021.08.26. \
            This date will be the date the recommender model was run and we \
                will use the resulting tickers for our proof",
    )

    saveMonth = str(report_date)[:7]
    saveReport_port_results = Path(f"reports/port_results/{saveMonth}/{report_date}/")
    saveReport_portfolio = Path(f"reports/portfolio/{saveMonth}/{report_date}/")

    r_stocks = list(pd.read_csv(saveReport_port_results / f"proof.csv")["symbol"])
    st.write(f"** - Below Are The Selected Stocks - total stocks = [{len(r_stocks)}]**")
    st.text(r_stocks)
    st.sidebar.write(" *" * 25)
    return r_stocks


def recommended_stocks_2():
    sdate = date(2021, 7, 15)  # start date
    edate = datetime.now()
    date_range_lst = list(pd.date_range(sdate, edate - timedelta(days=1), freq="d"))
    report_date = st.sidebar.date_input(
        label="> recommender date:",
        value=date(2021, 7, 15),
        min_value=sdate,
        max_value=edate,
        key="date to run proof",
        help="Select a date in the range between 2021.07.15 - 2021.08.26. \
            This date will be the date the recommender model was run and we \
                will use the resulting tickers for our proof",
    )
    r_stocks = list(
        pd.read_pickle(
            f"data/recommenders/{report_date}/recommender_final_return_dataFrame.pkl"
        )["Symbol"]
    )
    st.write(f"** - Below Are The Selected Stocks - total stocks = [{len(r_stocks)}]**")
    st.text(r_stocks)
    st.sidebar.write(" *" * 25)
    return r_stocks


def display_as_percent(val):
    return str(round(val * 100, 1)) + "%"


def company_longName(symbol):
    d = Ticker(symbol).quote_type
    return list(d.values())[0]["longName"]


def time_fixer(obj):
    x = ""
    y = list(str(obj))[:10]
    for i in y:
        x += i
    return x


def generate_household_watch_list(a_lst, b_lst, c_lst):
    one = a_lst + b_lst
    two = one + c_lst
    three = list(set(two))
    four = sorted(three)
    five = ""
    for i in four:
        five += i + " "
    return five


def stock_selection(ex_lst):
    st.sidebar.write("**Enter Your Stocks**")
    st.sidebar.markdown(
        f" \n\
    - ** Personal Portfolio** or **Single Stock** \n \
    - Seperated each ticker with a space"
    )
    st.sidebar.write("** Example:** ")
    # personal_portfolio = st.sidebar.text_input("",value=ex_lst)
    # personal_portfolio = personal_portfolio.split()
    # if type(personal_portfolio) == list:
    #     if personal_portfolio:
    #         st.sidebar.write(
    #             f"\n \
    #             - **Personal Portfolio Entry Validated**"
    #         )
    # return personal_portfolio


def open_webpage(site):
    try:  # Open URL in a new tab, if a browser window is already open.
        webbrowser.open_new_tab(site)
    except Exception:  # Open URL in new window, raising the window if possible.
        webbrowser.open_new(site)


def stages(round_df, round_count, total_asset_count):
    new_asset_count = len(round_df["Symbol"])
    st.subheader(f"** > Round {round_count} Results**")
    st.write(f"** - Total Assets Pass Round {round_count} = [{new_asset_count:,d}] **")
    st.write(
        f"** - Success · Rate = [{round((new_asset_count / total_asset_count) * 100, 2)}%]**"
    )
    st.dataframe(round_df)
    st.write("__" * 25)


def build_portfolio_options(data):
    st.subheader("** > Final 'Short List' Returned From Total Market Screener**")
    st.dataframe(data)
    lst_of_returns = p1.portfolio_optimizer(list(data["Symbol"])).optimize()
