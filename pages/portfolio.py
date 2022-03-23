import streamlit as st
import webbrowser
from datetime import datetime
from pathlib import Path
import pandas as pd
from os.path import exists
import numpy as np
import matplotlib.pyplot as plt
from yahooquery import Ticker

import src.models.portfolio as p1
from src.tools import functions as f0
from src.tools import lists as l0
from src.tools import scripts as s0
from src.tools import widgets as w0

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


optimizer_web_page_1 = "\n\
    - https://www.investopedia.com/terms/m/modernportfoliotheory.asp \n\
    - https://www.investopedia.com/terms/e/efficientfrontier.asp#:~:text=The%20efficient%20frontier%20is%20the,for%20the%20level%20of%20risk."
optimizer_definition_script = "\
    * Portfolio optimization is the process of selecting the best portfolio (asset distribution),\
    out of the set of all portfolios being considered, according to some objective. The objective\
    typically maximizes factors such as expected return, and minimizes costs like financial risk.\
    * Modern portfolio theory (MPT) is a theory on how risk-averse investors can construct portfolios\
    to maximize expected return based on a given level of market risk.\
    Harry Markowitz pioneered this theory in his paper 'Portfolio Selection,'\
    which was published in the Journal of Finance in 1952."

optimizer_keys = "> Key Assumptions of Modern Portfolio Theory "
optimizer_details_script = "\
    * At the heart of MPT is the idea that risk and return are directly linked. \
    This means that an investor must take on a higher level of risk to achieve greater expected returns."



class Portfolio(object):


    def __init__(self, today_stamp):
        self.today_stamp = today_stamp
        self.saveMonth = str(datetime.now())[:7]

        self.saveRec = Path(f"data/recommenders/{str(today_stamp)[:4]}/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveRec.exists():
            self.saveRec.mkdir(parents=True)

        self.saveTickers = Path(f"data/tickers/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveTickers.exists():
            self.saveTickers.mkdir(parents=True)

        self.savePlots = Path(f"data/plots/{self.saveMonth}/{self.today_stamp}/")
        if not self.savePlots.exists():
            self.savePlots.mkdir(parents=True)            

                

        methodology = st.sidebar.radio('pick method', ('Defaults', 'Auto Config', 'Pick Parameters'))

        if methodology == "Defaults":
            initial_investment = 2500.00
            min_composite_score = 60.0
            num_portfolios = 13000
            max_allocations = 15.0
            min_Sentiment_Score = 13.0
            min_Analyst_Recom_score = 70.0
            min_RS_Rating_score = 80.0

        if methodology == "Auto Config":
            initial_investment = 2500.00
            min_composite_score = np.random.randint(50, 70)
            num_portfolios = np.random.randint(13000, 34000)
            max_allocations = np.random.randint(9, 49)
            min_Sentiment_Score = np.random.randint(1, 25)
            min_Analyst_Recom_score = np.random.randint(59, 89)
            min_RS_Rating_score = np.random.randint(70, 91)

        elif methodology == "Pick Parameters":
            initial_investment = st.sidebar.number_input(
                label="Enter Initial Investment Amount ($)",
                value=2500.0,
                min_value=100.0,
                max_value=25000.0,
                key="initial_investment",
            )
            min_composite_score = st.sidebar.number_input(
                label="Set Lowest Acceptable Composite Score ",
                value=60.00,
                min_value=1.0,
                max_value=100.1,
                key="min_composite_score",
            )
            min_Analyst_Recom_score = st.sidebar.number_input(
                label="Set Lowest Acceptable Adj Analyst Score ",
                value=70.0,
                min_value=50.00,
                max_value=106.51,
                key="min_composite_score",
            )
            min_RS_Rating_score = st.sidebar.number_input(
                label="Set Lowest Acceptable RSI Score ",
                value=80.0,
                min_value=50.00,
                max_value=100.1,
                key="min_composite_score",
            )
            min_Sentiment_Score = st.sidebar.number_input(
                label="Set Lowest Acceptable Sentiment Score ",
                value=10.00,
                min_value=1.0,
                max_value=100.1,
                key="min_composite_score",
            )
            max_allocations = st.sidebar.number_input(
                label="Set Max Allocation Per Stock",
                value=15.00,
                min_value=1.0,
                max_value=49.99,
                key="max_allocations",
            )
            st.sidebar.caption(
                "__ * Risk·Free·Rate - 10·yr T-bill: 1.48% (10.2.2021)__\n\n"
            )
            st.sidebar.header("__[4] BUILD PORTFOLIO:__")


            # self.recommender_dataset = self.recommender_dataset[self.recommender_dataset["my_score"] >= min_composite_score]
            # self.recommender_dataset = self.recommender_dataset[self.recommender_dataset["RS_Rating"] >= min_RS_Rating_score]
            # self.recommender_dataset = self.recommender_dataset[self.recommender_dataset["Sentiment_Score"]>= min_Sentiment_Score]
            # self.recommender_dataset = self.recommender_dataset[self.recommender_dataset["adj_analyst_recom"]>= min_Analyst_Recom_score]

            




    def run_pca(self, ticker_list, report_date):
        st.header(" > Principal Component Analysis (PCA)")
        st.write(" * __General Analysis Definitions:__")
        """
            * Principal Component Analysis, or PCA, is a dimensionality-reduction method that is
            often used to reduce the dimensionality of large data sets, by transforming a large set of
            variables into a smaller one that still contains most of the information in the large set.
        """

        pca_web_page = "https://towardsdatascience.com/a-one-stop-shop-for-principal-component-analysis-5582fb7e0a9c"
        if st.button("Open Principal Component Analysis (PCA) Web Page"):
            webbrowser.open_new_tab(pca_web_page)

        st.write(f"* __Selected Stock Portfolio: [{len(ticker_list)}]__")
        st.text(ticker_list)
        st.write(f"{'_'*25}")

        if st.sidebar.button("Run Mod"):
            hammerTime = Ticker(
                ticker_list,
                asynchronous=True,
                formatted=False,
                backoff_factor=0.34,
                progress=True,
                validate=True,
                verify=True,
            )
            hammer_hist = hammerTime.history(period='2y').reset_index().set_index('date')
            hammer_hist.index = pd.to_datetime(hammer_hist.index)
            hammer_hist = hammer_hist.rename(columns={'symbol': 'ticker'})         
            bulk_files = pd.DataFrame()
            for i in ticker_list:
                try:
                    z = pd.DataFrame(hammer_hist[hammer_hist['ticker'] == i]['adjclose'])
                    bulk_files[i] = z
                except:
                    print(f"failed ticker {i}")
                    ticker_list.remove(i)                       
            best = p1.pca_analysis(ticker_list, report_date, save_final=True, x_factor=1.0).build_pca(bulk_files)


    def run_randomForest(self, ticker_list):
        st.header(" > Random Forest (RF)")
        st.write(f"* __Selected Stock Portfolio: [{len(ticker_list)}]__")
        st.text(ticker_list)
        st.write(f"{'_'*25}")

        if st.sidebar.button("Run Mod"):
            p1.random_forest(ticker_list).plot_plot_roc()              



    def monteCarloCholesky(self, ticker_list, report_date="2021-09-30"):
        st.header(" > Monte Carlo Cholesky Simulation")

        st.write(f"* __Selected Stock Portfolio: [{len(ticker_list)}]__")
        st.text(ticker_list)
        st.write(f"{'_'*25}")

        if st.sidebar.button("Run Mod"):
            no_trials = 1300
            p1.MonteCarloCholesky(report_date).montecarlo_cholesky(
                tickers=ticker_list,
                days=252,
                iterations=no_trials,
                start="2011-1-1",
                show_hist=True,
            )
            fin = p1.MonteCarloCholesky(
                report_date
            ).montecarlo_sharpe_optimal_portfolio(
                tickers=ticker_list, trials=no_trials, end_date=report_date
            )
            fin.columns = ["symbol", "allocation"]
            st.dataframe(fin)
            p1.Proof_of_Concept_000(report_date).setup(fin, 2500)

    def run_efficientFrontier(self, ticker_list):
        st.header(" > Markowitz Efficient Frontier")
        st.write(" * __General Analysis Definitions:__ ")
        """
            * In modern portfolio theory, the efficient frontier is an investment portfolio which occupies the efficient
            part of the risk–return spectrum. Formally, it is the set of portfolios which satisfy the
            condition that no other portfolio exists with a higher expected return but with the same
            standard deviation of return.
            * The efficient frontier is the set of optimal portfolios that offer the highest expected return for a \
            defined level of risk or the lowest risk for a given level of expected return. \
            Portfolios that lie below the efficient frontier are sub-optimal because they do not \
            provide enough return for the level of risk.
        """

        st.write(f"* __Selected Stock Portfolio: [{len(ticker_list)}]__")
        st.text(ticker_list)
        st.write(f"{'_'*25}")

        markowitz_efficientFrontier_web_page = (
            "https://www.investopedia.com/terms/e/efficientfrontier.asp"
        )
        if st.button("Open Markowitz Efficient Frontier Web Page"):
            webbrowser.open_new_tab(markowitz_efficientFrontier_web_page)
        st.write("__" * 25)

        st.sidebar.subheader("> Step #4")
        if st.sidebar.button("Run Efficient Frontier"):
            p1.efficient_frontier(RISKY_ASSETS=ticker_list).final_plot()
            st.write(" *" * 25)

    def run_optimizer(self, ticker_list, report_date):
        st.header(" > Modern Portfolio Theory ~ Portfolio Optimization ")
        with st.expander("Expand", expanded=False):
            clicked = w0.widget_header(
                optimizer_web_page_1, " > Definitions", optimizer_definition_script
            )
            clicked = w0.widget_analysis(optimizer_keys, optimizer_details_script)
        if st.sidebar.button("Run Mod"):
            p1.portfolio_optimizer(ticker_list).optimize()

    # ----------------------------------------------------------------------------------------- > stage: [PORTFOLIO]

    def run_portfolio(self):
        st.header("[Portfolio]")
        st.write(f"{'_'*25} \n {'_'*25}")

        model = st.sidebar.radio("Choose A Model", l0.feature_portfolio)
        options_f = ["Personal Portfolio", "Recommended Stocks"] #"Ticker Lists"]
        tickers = st.sidebar.radio("Model List:", options_f)
        st.sidebar.write(" *" * 25)

        if tickers == "Personal Portfolio":
            ex_lst = "AAPL ASML NVDA TSLA SNOW"
            f0.stock_selection(ex_lst)
            personal_stocks = st.sidebar.text_input("", value=ex_lst)
            personal_stocks = personal_stocks.split()

            if model == "Principal Component Analysis":
                self.run_pca(personal_stocks, self.today_stamp)

            if model == "Random Forest":
                self.run_randomForest(personal_stocks)

            if model == "Monte Carlo Cholesky":
                self.monteCarloCholesky(personal_stocks)

            if model == "Efficient Frontier":
                self.run_efficientFrontier(personal_stocks)

            if model == "Portfolio Optimizer":
                self.run_optimizer(personal_stocks, self.today_stamp)

        if tickers == "Recommended Stocks":
            name_lst = st.sidebar.radio("",
                [
                    # 'markowitz_random',
                    'minimum_volatility_portfolio',    
                    'maximum_sharpe_ratio',
                    # 'minimum_volatility_random',
                    'maximum_sharpe_equalWT',
                    'monte_carlo_cholesky',

                    # 'max_sharpe_df_1',
                    # 'max_sharpe_df_3',
                    # 'min_vol_df_3',
                ]
            )
            final_rec_lst, report_date = f0.recommended_stocks_0(name_lst)

            if model == "Principal Component Analysis":
                self.run_pca(final_rec_lst, report_date)

            if model == "Random Forest":
                self.run_randomForest(final_rec_lst)

            if model == "Monte Carlo Cholesky":
                self.monteCarloCholesky(final_rec_lst, report_date)

            if model == "Efficient Frontier":
                self.run_efficientFrontier(final_rec_lst)

            if model == "Portfolio Optimizer":
            
                self.run_optimizer(final_rec_lst, report_date)

        if tickers == "Ticker Lists":
            st.sidebar.header("[Step # 4]")
            st.sidebar.subheader("Select stocks To Run")
            stock_lsts = st.sidebar.radio("Stock Lists:", l0.stock_name_list)
            st.sidebar.write(f"{'__'*25} \n {'__'*25}")

            tic_lst = list(
                pd.read_pickle(self.saveTickers / f"{stock_lsts}.pkl")["Symbol"]
            )

            if model == "Principal Component Analysis":
                self.run_pca(tic_lst)

            if model == "Random Forest":
                self.run_randomForest(tic_lst)

            if model == "Monte Carlo Cholesky":
                self.monteCarloCholesky(tic_lst)

            if model == "Efficient Frontier":
                self.run_efficientFrontier(tic_lst)

            if model == "Portfolio Optimizer":
                self.run_optimizer(tic_lst, self.today_stamp)
