# --------------------------------------------------------- > stage: [LIBRARY IMPORT]
import sys
import warnings

warnings.filterwarnings("ignore")
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
import streamlit as st
import tensorflow as tf

import pages as p1
from src.tools import functions as f0
from src.tools import lists as l0
from src.tools import scripts as s0
from src.tools import widgets as w0
import os


try:
    st.set_page_config(
        page_title="the only app in town",
        page_icon="chart_with_upwards_trend",
        layout="wide",
        initial_sidebar_state="expanded",
    )
except:
    pass
warnings.filterwarnings("ignore")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {
                visibility: hidden;
                }
            footer:after {
                # content:'__~ Created By: G.D.P. ~__'; 
                visibility: visible;
                display: block;
                position: relative;
                #background-color: red;
                padding: 30px;
                top: 2px;
            }            
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.set_option("deprecation.showPyplotGlobalUse", False)

pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", -1)
pd.options.display.float_format = "{:,}".format

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

gpu_devices = tf.config.experimental.list_physical_devices("GPU")
if gpu_devices:
    print("Using GPU")
    tf.config.experimental.set_memory_growth(gpu_devices[0], True)
    tf.config.experimental.set_synchronous_execution(enable=True)
    tf.config.experimental.enable_mlir_bridge()
    tf.config.experimental.enable_tensor_float_32_execution(enabled=True)
    tf.config.threading.get_inter_op_parallelism_threads()
    tf.config.threading.set_inter_op_parallelism_threads(0)
else:
    print("Using CPU")
os.environ["NUMEXPR_MAX_THREADS"] = "20"
os.environ["NUMEXPR_NUM_THREADS"] = "10"


# ------------------------------------------------------------ > page: [LOGIN_PG]


def page_login(today_stamp):
    authUser = p1.Credentials(today_stamp).check_password()
    return authUser


# ------------------------------------------------------------ > page: [HOME_PAGE]


def page_home():
    p1.Home(l0.general_pages).run_home()


# ------------------------------------------------------------ > page: [HOME_PAGE]


def page_auto_advisor():
    p1.Review_Your_Portfolio(today_stamp).collect_portfolio()


# ------------------------------------------------------------ > page: [SNAPSHOT]


def page_snapshot(today_stamp):
    p1.Snapshot(today_stamp).run_mkt_snap()


# ------------------------------------------------------------ > page: [PROOF]


def page_proof():
    p1.Proof().prove_it()


# ------------------------------------------------------------ > page: [PROOF]


def huddle_up():
    st.header("coming soon")


# ------------------------------------------------------------ > page: [BACKTEST]


def page_backtest():
    p1.Backtest().backtest_1()


# ------------------------------------------------------------ > page: [FORECAST]


def page_forecast(today_stamp):
    p1.Forecast(today_stamp).run_forecast()


# ------------------------------------------------------------ > page: [STRATEGY]


def page_strategy(today_stamp):
    p1.Strategy(today_stamp).run_the_strats()


# ------------------------------------------------------------ > page: [ANALYSIS]


def page_analysis(today_stamp):
    p1.Analysis(today_stamp).run_analysis()


# ------------------------------------------------------------ > page: [RECOMMENDER]


def page_recommender(today_stamp):
    p1.Recommender(today_stamp).run_recommender()


# ------------------------------------------------------------ > page: [PORTFOLIO]


def page_portfolio(today_stamp):
    p1.Portfolio(today_stamp).run_portfolio()


# ------------------------------------------------------------ > page: [TEST]


def page_test_env(today_stamp, edate):
    p1.Test().run_test()
    p1.Test_Env(edate).build_test()


# ------------------------------------------------------------ > page: [TEST]


def mode_auto_advisor(today_stamp):
    p1.Review_Your_Portfolio(today_stamp).collect_portfolio()


# ------------------------------------------------------------ > page: [RUN]


if __name__ == "__main__":

    # today_stamp = str(datetime.now())[:10]
    today_stamp = "2021-10-02"

    # if page_login(today_stamp):
    if 1 > 0:

        st.sidebar.title("__ · NAVIGATION · __")
        st.sidebar.markdown(f"{'__'*25} \n {'__'*25} \n")
        st.sidebar.caption(s0.navGuide_a)
        st.sidebar.caption(f"{'__'*25} \n {'__'*25} ")
        st.sidebar.caption(s0.navGuide_b)

        st.sidebar.header("__[1] Select App Section__")
        st.sidebar.caption("- __Navigate pages using the drop-down-box below__")
        systemStage = st.sidebar.radio("", l0.general_pages, key="nunya")
        st.sidebar.write(f"{'__'*25}\n {'__'*25}")

        if systemStage == "Home":
            page_home()

        if systemStage == "Auto Advisor":
            page_auto_advisor()

        if systemStage == "Snapshot":
            page_snapshot(today_stamp)

        if systemStage == "Proof":
            page_proof()

        if systemStage == "Huddle-Up":
            huddle_up()

        if systemStage == "Backtest":
            page_backtest()

        if systemStage == "Strategy":
            page_strategy(today_stamp)

        if systemStage == "Forecast":
            page_forecast(today_stamp)

        if systemStage == "Analysis":
            page_analysis(today_stamp)

        if systemStage == "Recommender":
            page_recommender(today_stamp)

        if systemStage == "Portfolio":
            page_portfolio(today_stamp)

        if systemStage == "test_env":
            page_test_env()
