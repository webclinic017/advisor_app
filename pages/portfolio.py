import streamlit as st
import webbrowser
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np
from yahooquery import Ticker

import src.models.portfolio as p1
from src.tools import functions as f0
from src.tools import lists as l0
from src.tools import scripts as s0
from src.tools import widgets as w0



optimizer_web_page_1 = "\n\
    - https://www.investopedia.com/terms/m/modernportfoliotheory.asp \n\
    - https://www.investopedia.com/terms/e/efficientfrontier.asp"
optimizer_definition_script = "\
    * Portfolio optimization is the process of selecting the best portfolio (asset distribution),\
    out of the set of all portfolios being considered, according to some objective. The objective\
    typically maximizes factors such as expected return, and minimizes costs like financial risk.\
    * Modern portfolio theory (MPT) is a theory on how risk-averse investors can construct portfolios\
    to maximize expected return based on a given level of market risk.\
    Harry Markowitz pioneered this theory in his paper 'Portfolio Selection,'\
    which was published in the Journal of Finance in 1952."

optimizer_keys = "▷ Key Assumptions of Modern Portfolio Theory"
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


    def run_pca(self, ticker_list, report_date):
        st.header("𝄖𝄗𝄘𝄙𝄚 ▷ Principal Component Analysis (PCA) ◁ 𝄚𝄙𝄘𝄗𝄖")
        cols = st.columns(2)
        with cols[0]:       
            with st.expander("▷ Details:", expanded=False):                    
                st.caption(f"\
                    * Principal Component Analysis, or PCA, is a dimensionality-reduction method that is \
                    often used to reduce the dimensionality of large data sets, by transforming a large set of \
                    variables into a smaller one that still contains most of the information in the large set. "
                    )
                st.caption(f"{' '*25}")
                pca_web_page = "https://towardsdatascience.com/a-one-stop-shop-for-principal-component-analysis-5582fb7e0a9c"
                if st.button("Open Principal Component Analysis (PCA) Web Page"):
                    webbrowser.open_new_tab(pca_web_page)
        st.header(f"{'𝄖'*33}")
        
        if st.sidebar.button("[ 4 ] Run Mod"):
            st.subheader(f"𝄖𝄗𝄘𝄙𝄚 Selected Stock Portfolio: [{len(ticker_list)}]")
            st.markdown(f"* {ticker_list}")
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
            p1.pca_analysis(ticker_list, report_date, save_final=True).build_pca(bulk_files)
            st.subheader("𝄖𝄗𝄘𝄙𝄚 Forecast Complete")


    def run_randomForest(self, ticker_list):
        st.header("𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄚𝄚 ▷ Random Forest (RF) ◁ 𝄚𝄚𝄙𝄙𝄘𝄘𝄗𝄗𝄖")
        st.header(f"{'𝄖'*33}")

        if st.sidebar.button("Run Mod"):
            st.subheader(f"𝄖𝄗𝄘𝄙𝄚 Selected Stock Portfolio: [{len(ticker_list)}]")
            st.markdown(f"* {ticker_list}")            
            p1.random_forest(ticker_list).plot_plot_roc()              



    def monteCarloCholesky(self, ticker_list, report_date="2021-09-30"):
        st.header("𝄖𝄗𝄘𝄙𝄚 ▷ Monte Carlo Cholesky Simulation ◁ 𝄚𝄙𝄘𝄗𝄖")
        st.header(f"{'𝄖'*33}")

        if st.sidebar.button("Run Mod"):
            st.subheader(f"__𝄖𝄗𝄘𝄙𝄚 Selected Stock Portfolio: [{len(ticker_list)}]__")
            st.markdown(f"* {ticker_list}")            
            st.caption('_'*20)
            no_trials = 1300
            p1.MonteCarloCholesky(report_date).montecarlo_cholesky(
                tickers=ticker_list,
                days=252,
                iterations=no_trials,
                start="2011-1-1",
                show_hist=True,
                )
            fin = p1.MonteCarloCholesky(report_date).montecarlo_sharpe_optimal_portfolio(tickers=ticker_list, trials=no_trials, end_date=report_date)
            fin.columns = ["symbol", "allocation"]
            st.dataframe(fin)


    def run_efficientFrontier(self, ticker_list):
        st.header("𝄖𝄖𝄗𝄗𝄘𝄙𝄚 ▷ Markowitz Efficient Frontier ◁ 𝄚𝄙𝄘𝄗𝄗𝄖𝄖")
        cols = st.columns(2)
        with cols[0]:       
            with st.expander("▷ Details:", expanded=False):            
                st.caption("\
                    * In modern portfolio theory, the efficient frontier is an investment portfolio which occupies the efficient\
                        part of the risk–return spectrum. Formally, it is the set of portfolios which satisfy the \
                        condition that no other portfolio exists with a higher expected return but with the same \
                        standard deviation of return. \n\n\
                    * The efficient frontier is the set of optimal portfolios that offer the highest expected return for a \
                        defined level of risk or the lowest risk for a given level of expected return. \
                        Portfolios that lie below the efficient frontier are sub-optimal because they do not \
                        provide enough return for the level of risk. \n\n"
                )
                markowitz_efficientFrontier_web_page = ("https://www.investopedia.com/terms/e/efficientfrontier.asp")
                if st.button("Open Markowitz Efficient Frontier Web Page"):
                    webbrowser.open_new_tab(markowitz_efficientFrontier_web_page)                
        st.header(f"{'𝄖'*33}")   
        if st.sidebar.button("[ 4 ] Run Efficient Frontier"):
            st.subheader(f"𝄖𝄗𝄘𝄙𝄚 Selected Stock Portfolio: [{len(ticker_list)}]")
            st.markdown(f"* {ticker_list}")               
            p1.efficient_frontier(RISKY_ASSETS=ticker_list).final_plot()


    def run_optimizer(self, ticker_list, report_date):
        st.header("𝄖𝄗𝄘𝄙𝄚 ▷ Modern Portfolio Theory & Optimization ◁ 𝄚𝄙𝄘𝄗𝄖")
        cols = st.columns(2)
        with cols[0]:       
            with st.expander("▷ Details:", expanded=False):            
                clicked = w0.widget_header2(optimizer_definition_script)                                    
                clicked = w0.widget_analysis2(optimizer_keys, optimizer_details_script)
                if st.button("▷ Modern Portfolio Theory | Investopedia"):
                    webbrowser.open_new_tab("https://www.investopedia.com/terms/m/modernportfoliotheory.asp")
                if st.button("▷ Efficient Frontier | Investopedia"):
                    webbrowser.open_new_tab("https://www.investopedia.com/terms/e/efficientfrontier.asp")                
        st.header(f"{'𝄖'*33}")   
        if st.sidebar.button("Run Mod"):
            p1.portfolio_optimizer(ticker_list).optimize()

    # ----------------------------------------------------------------------------------------- > stage: [PORTFOLIO]

    def run_portfolio(self):
        st.header("◾ 𝄖𝄖𝄖𝄖𝄗𝄗𝄗𝄗𝄘𝄘𝄘𝄙𝄙𝄚 · Portfolio · 𝄚𝄙𝄙𝄘𝄘𝄘𝄗𝄗𝄗𝄗𝄖𝄖𝄖𝄖 ◾")
        st.header(f"{' '*25}")                   

        model = st.sidebar.selectbox("[ 2 ] Choose A Model", l0.feature_portfolio)
        
        ex_lst = "AAPL ALB AMD AMZN ASML GOOGL NVDA TSLA SNOW SEDG REGN WMT VZ"
        personal_stocks = st.sidebar.text_input("[ 3 ] Enter Portfolio (capital tickers, seperate with space)", help=f"Example: {ex_lst}", value=ex_lst)
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



        # methodology = st.sidebar.selectbox('[ 2 ] Select Method', ('Defaults', 'Auto Config', 'Pick Parameters'))

        # if methodology == "Defaults":
        #     initial_investment = 2500.00
        #     min_composite_score = 60.0
        #     num_portfolios = 13000
        #     max_allocations = 15.0
        #     min_Sentiment_Score = 13.0
        #     min_Analyst_Recom_score = 70.0
        #     min_RS_Rating_score = 80.0

        # if methodology == "Auto Config":
        #     initial_investment = 2500.00
        #     min_composite_score = np.random.randint(50, 70)
        #     num_portfolios = np.random.randint(13000, 34000)
        #     max_allocations = np.random.randint(9, 49)
        #     min_Sentiment_Score = np.random.randint(1, 25)
        #     min_Analyst_Recom_score = np.random.randint(59, 89)
        #     min_RS_Rating_score = np.random.randint(70, 91)

        # elif methodology == "Pick Parameters":
        #     initial_investment = st.sidebar.number_input(
        #         label="Enter Initial Investment Amount ($)",
        #         value=2500.0,
        #         min_value=100.0,
        #         max_value=25000.0,
        #         key="initial_investment",
        #     )
        #     min_composite_score = st.sidebar.number_input(
        #         label="Set Lowest Acceptable Composite Score ",
        #         value=60.00,
        #         min_value=1.0,
        #         max_value=100.1,
        #         key="min_composite_score",
        #     )
        #     min_Analyst_Recom_score = st.sidebar.number_input(
        #         label="Set Lowest Acceptable Adj Analyst Score ",
        #         value=70.0,
        #         min_value=50.00,
        #         max_value=106.51,
        #         key="min_composite_score",
        #     )
        #     min_RS_Rating_score = st.sidebar.number_input(
        #         label="Set Lowest Acceptable RSI Score ",
        #         value=80.0,
        #         min_value=50.00,
        #         max_value=100.1,
        #         key="min_composite_score",
        #     )
        #     min_Sentiment_Score = st.sidebar.number_input(
        #         label="Set Lowest Acceptable Sentiment Score ",
        #         value=10.00,
        #         min_value=1.0,
        #         max_value=100.1,
        #         key="min_composite_score",
        #     )
        #     max_allocations = st.sidebar.number_input(
        #         label="Set Max Allocation Per Stock",
        #         value=15.00,
        #         min_value=1.0,
        #         max_value=49.99,
        #         key="max_allocations",
        #     )
        #     st.sidebar.caption(
        #         "__ * Risk·Free·Rate - 10·yr T-bill: 1.48% (10.2.2021)__\n\n"
        #     )
        #     st.sidebar.header("__[4] BUILD PORTFOLIO:__")


        #     # self.recommender_dataset = self.recommender_dataset[self.recommender_dataset["my_score"] >= min_composite_score]
        #     # self.recommender_dataset = self.recommender_dataset[self.recommender_dataset["RS_Rating"] >= min_RS_Rating_score]
        #     # self.recommender_dataset = self.recommender_dataset[self.recommender_dataset["Sentiment_Score"]>= min_Sentiment_Score]
        #     # self.recommender_dataset = self.recommender_dataset[self.recommender_dataset["adj_analyst_recom"]>= min_Analyst_Recom_score]