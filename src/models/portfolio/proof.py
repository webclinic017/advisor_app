from os.path import exists
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
from pathlib import Path
from pathlib import Path
import streamlit as st
import yfinance as yf
import pickle
import csv

from src.tools.functions import company_longName
from src.models.portfolio.proof_port import The_Portfolio_Optimizer

pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)
pd.options.display.float_format = "{:,}".format





class Proof_of_Concept_Viewer(object):

    def __init__(self, report_date):
        self.report_date = str(report_date)[:10]
        self.saveMonth = str(self.report_date)[:7]
        self.saveRec = Path(f"data/recommenders/{self.saveMonth}/{self.report_date}/")
        self.saveReport = Path(f"reports/portfolio/{self.saveMonth}/{self.report_date}/")
        self.final_loc = Path(f"reports/port_results/{self.saveMonth}/{self.report_date}/")


    def setup(self, initial_cash=5000):
        gdp = pd.read_csv(self.final_loc / "gdp.csv")
        proof_spy = pd.read_csv(self.final_loc / "proof_spy.csv").set_index("SPY")
        proof = pd.read_csv(self.final_loc / "proof.csv").set_index("rank")
        zzz = pd.DataFrame(pd.read_csv((self.saveReport / f"roll_out_list_a.csv")))
        gdp_b = pd.read_csv(self.final_loc / "gdp_b.csv")
        proof_b = pd.read_csv(self.final_loc / "proof_b.csv").set_index("rank")
        gdp_c = pd.read_csv(self.final_loc / "gdp_c.csv")
        proof_c = pd.read_csv(self.final_loc / "proof_c.csv").set_index("rank")
        gdp_d = pd.read_csv(self.final_loc / "gdp_d.csv")
        proof_d = pd.read_csv(self.final_loc / "proof_d.csv").set_index("rank")

        self.initial_cash = int((initial_cash * proof["allocation"].sum()) / 100)
        beat_num = proof_spy["return"][0]
        proof_2 = proof[proof["return"] > 0.0]
        proof_3 = proof[proof["return"] > beat_num]
        winning_percentage = round((len(proof_2["symbol"]) / len(proof["symbol"])) * 100, 2)
        beat_spy_percentage = round((len(proof_3["symbol"]) / len(proof["symbol"])) * 100, 2)
        total_act_return = round((proof["cash_now"].sum()), 2)
        act_ror = round(((total_act_return - self.initial_cash) / self.initial_cash) * 100, 2)
        st.header(f"** > The Facts: [MAX SHARPE RATIO] **")
        st.write(f" - Start Position [{self.report_date}] ")
        st.write(f" - Today's Position [{str(datetime.now())[:10]}] ")
        st.table(gdp)
        st.write("__" * 25)
        st.header(f"** > Proof returns**")
        st.write(f" - equally weighted portfolio")
        st.write(
            f"\
            - Winning Stock Picks [Positive Return] = \
                {len(proof_2['symbol'])}/{len(proof['symbol'])}, [{winning_percentage}%] "
        )
        st.write(
            f"\
            - Stocks Outperforming The SPY  = \
                {len(proof_3['symbol'])}/{len(proof['symbol'])}, [{beat_spy_percentage}%   ]]"
        )
        st.write(f"** > Initial Portfolio Optimization Modeled On {self.report_date}**")

        if exists(self.saveReport / f"roll_out_list_a.pkl"):
            zzz = pd.DataFrame(pd.read_csv(self.saveReport / f"roll_out_list_a.csv"))        
        print(zzz)


        zzz.columns = ["A", "B"]
        lst = list(zzz["B"])
        lst_a = lst[:4]
        lst_b = lst[5:9]
        for i in lst_a[1:]:
            st.write(f" - {i}")
        st.table(proof)


        self.initial_cash = initial_cash * proof_b["allocation"].sum()
        beat_num = proof_spy["return"][0]
        proof_2 = proof_b[proof_b["return"] > 0.0]
        proof_3 = proof_b[proof_b["return"] > beat_num]
        winning_percentage = round((len(proof_2["symbol"]) / len(proof_b["symbol"])) * 100, 2)
        beat_spy_percentage = round((len(proof_3["symbol"]) / len(proof_b["symbol"])) * 100, 2)
        total_act_return = round((proof["cash_now"].sum()), 2)
        act_ror = round(((total_act_return - self.initial_cash) / self.initial_cash) * 100, 2)
        st.header(f"** > The Facts: [MIN VOLATILITY]**")
        st.write(f" - Start Position [{self.report_date}] ")
        st.write(f" - Today's Position [{str(datetime.now())[:10]}] ")
        st.table(gdp_b)
        st.write("__" * 25)

        st.header(f"** > Proof returns**")
        st.write(f" - equally weighted portfolio")
        st.write(
            f" - Winning Stock Picks [Positive Return] =\
             {len(proof_2['symbol'])}/{len(proof_b['symbol'])}, [{winning_percentage}%] ")
        st.write(
            f" - Stocks Outperforming The SPY  =\
             {len(proof_3['symbol'])}/{len(proof_b['symbol'])}, [{beat_spy_percentage}%   ]]")
        st.table(proof_b)

        self.initial_cash = initial_cash * proof_c["allocation"].sum()
        beat_num = proof_spy["return"][0]
        proof_2 = proof_c[proof_c["return"] > 0.0]
        proof_3 = proof_c[proof_c["return"] > beat_num]
        winning_percentage = round(
            (len(proof_2["symbol"]) / len(proof_c["symbol"])) * 100, 2
        )
        beat_spy_percentage = round(
            (len(proof_3["symbol"]) / len(proof_c["symbol"])) * 100, 2
        )
        total_act_return = round((proof["cash_now"].sum()), 2)
        act_ror = round(
            ((total_act_return - self.initial_cash) / self.initial_cash) * 100, 2
        )
        st.header(f"** > The Facts: [Near Equal Wt - Random Sharpe]**")
        st.write(f" - Start Position [{self.report_date}] ")
        st.write(f" - Today's Position [{str(datetime.now())[:10]}] ")
        st.table(gdp_c)
        st.write("__" * 25)
        st.header(f"** > Proof returns**")
        st.write(f" - Near Equal Wt - Random Sharpe")
        st.write(
            f" - Winning Stock Picks [Positive Return] = \
            {len(proof_2['symbol'])}/{len(proof_c['symbol'])}, [{winning_percentage}%] "
        )
        st.write(
            f" - Stocks Outperforming The SPY  = \
            {len(proof_3['symbol'])}/{len(proof_c['symbol'])}, [{beat_spy_percentage}%   ]]"
        )
        st.table(proof_c)

        self.initial_cash = initial_cash * proof_d["allocation"].sum()
        beat_num = proof_spy["return"][0]
        proof_2 = proof_d[proof_d["return"] > 0.0]
        proof_3 = proof_d[proof_d["return"] > beat_num]
        winning_percentage = round(
            (len(proof_2["symbol"]) / len(proof_d["symbol"])) * 100, 2
        )
        beat_spy_percentage = round(
            (len(proof_3["symbol"]) / len(proof_d["symbol"])) * 100, 2
        )
        total_act_return = round((proof["cash_now"].sum()), 2)
        act_ror = round(
            ((total_act_return - self.initial_cash) / self.initial_cash) * 100, 2
        )
        st.header(f"** > The Facts: [EQUALLY WEIGHTED]**")
        st.write(f" - Start Position [{self.report_date}] ")
        st.write(f" - Today's Position [{str(datetime.now())[:10]}] ")
        st.table(gdp_d)
        st.write("__" * 25)
        st.header(f"** > Proof returns**")
        st.write(f" - equally weighted portfolio")
        st.write(
            f" - Winning Stock Picks [Positive Return] = \
            {len(proof_2['symbol'])}/{len(proof_d['symbol'])}, [{winning_percentage}%] "
        )
        st.write(
            f" - Stocks Outperforming The SPY  =\
             {len(proof_3['symbol'])}/{len(proof_d['symbol'])}, [{beat_spy_percentage}%   ]]"
        )
        st.table(proof_d)
        return





class Proof_of_Concept(object):
    def __init__(self, report_date):
        self.report_date = str(report_date)[:10]
        self.saveMonth = self.report_date[:7]
        self.saveDay = str(datetime.now())[8:10]
        self.saveRec = Path(f"data/recommenders/{self.saveMonth}/{self.report_date}/")
        self.saveReport = Path(f"reports/portfolio/{self.saveMonth}/{self.report_date}/")
        self.file_loc = self.saveRec / f"recommender_final_return_dataFrame.pkl"


    def setup(self, portfolio_file, initial_cash=5000.0):
        portfolio_file = pd.DataFrame(portfolio_file.reset_index())
        divisor = len(portfolio_file["symbol"])
        proof = pd.DataFrame(portfolio_file[["symbol", "allocation"]]).sort_values("symbol")

        c = yf.download(list(proof["symbol"]), start=self.report_date)["Adj Close"]
        b = []
        for i in proof["symbol"]:
            b.append(company_longName(i))

        start_0 = proof["allocation"].sum() / 100
        self.initial_cash = int(float(initial_cash) * start_0)
        proof["companyName"] = b
        proof["start_price"] = list(c.iloc[0])
        proof["current_price"] = list(c.iloc[-1])
        proof = proof.dropna()
        proof["initial_investment"] = self.initial_cash * (proof["allocation"] / 100)
        proof["shares"] = round(proof["initial_investment"] / proof["start_price"], 2)
        proof["cash_now"] = round(proof["shares"] * proof["current_price"], 2)
        proof["return"] = round(
            (
                (proof["cash_now"] - proof["initial_investment"])
                / proof["initial_investment"]
            )
            * 100,
            2,
        )
        proof = proof.sort_values("return", ascending=False)
        proof["rank"] = range(1, len(proof["symbol"]) + 1)
        proof = proof.set_index("rank")

        fd = yf.download("SPY", start=self.report_date)
        og_price = round(fd["Adj Close"][0], 2)
        new_price = round(fd["Adj Close"][-1], 2)
        proof_spy = pd.DataFrame(["SPY"], columns=["SPY"])
        proof_spy["start_price"] = og_price
        proof_spy["current_price"] = new_price
        proof_spy["initial_investment"] = round(
            self.initial_cash / len(proof_spy["SPY"]), 2
        )
        proof_spy["shares"] = round(
            proof_spy["initial_investment"] / proof_spy["start_price"], 2
        )
        proof_spy["cash_now"] = round(
            proof_spy["shares"] * proof_spy["current_price"], 2
        )
        proof_spy["return"] = round(
            (
                (proof_spy["cash_now"] - proof_spy["initial_investment"])
                / proof_spy["initial_investment"]
            )
            * 100,
            2,
        )

        beat_num = proof_spy["return"][0]
        proof_2 = proof[proof["return"] > 0.0]
        proof_3 = proof[proof["return"] > beat_num]

        winning_percentage = round((len(proof_2["symbol"]) / divisor) * 100, 2)
        beat_spy_percentage = round((len(proof_3["symbol"]) / divisor),2)
        act_ror = round(
            (
                (proof["cash_now"].sum() - proof["initial_investment"].sum())
                / proof["initial_investment"].sum()
            )
            * 100,
            2,
        )

        gdp = pd.DataFrame(
            ["Recommended Stocks", "SPY Index"], columns=["strategy_vs_benchmark"]
        )
        gdp["starting_money"] = [
            f"${proof['initial_investment'].sum()}",
            f"${proof_spy['initial_investment'].sum()}",
        ]
        gdp["ending_money"] = [
            f"${proof['cash_now'].sum()}",
            f"${proof['cash_now'].sum()}",
        ]
        gdp["return"] = [
            f"{round(act_ror,2)}%",
            f"{round(float(proof_spy['return']),2)}%",
        ]
        gdp = gdp.set_index("strategy_vs_benchmark")

        st.caption(f"{'__'*25}\n{'__'*25}")
        st.header(f"> __The Facts: [MAX SHARPE RATIO]__")
        st.write(f" - Start Position [{self.report_date}] ")
        st.write(f" - Today's Position [{str(datetime.now())[:10]}] ")
        st.table(gdp)

        st.subheader(f"* __Proof returns__")
        st.write(f" - equally weighted portfolio")
        st.write(
            f" - Winning Stock Picks [Positive Return] = {len(proof_2['symbol'])}/{divisor}, [{winning_percentage}%] "
        )
        st.write(
            f" - Stocks Outperforming The SPY  = {len(proof_3['symbol'])}/{divisor}, [{beat_spy_percentage}%   ]]"
        )
        st.subheader(
            f"* __Initial Portfolio Optimization Modeled On {self.report_date}__"
        )

        if exists(self.saveReport / f"roll_out_list_a.pkl"):
            zzz = pd.DataFrame(pd.read_pickle(self.saveReport / f"roll_out_list_a.pkl"))
        else:
            zzz = pd.DataFrame(pd.read_csv(self.saveReport / f"roll_out_list_a.csv"))

        zzz=zzz.reset_index()
        zzz.columns = ["A", "B"]
        lst = list(zzz["B"])
        lst_a = lst[:4]
        lst_b = lst[5:9]
        for i in lst_a[1:]:
            st.write(f" - {i}")
        st.table(proof)
        st.caption(f"{'__'*25}\n{'__'*25}")

        gdp = pd.DataFrame(gdp)
        proof = pd.DataFrame(proof)
        proof_spy = pd.DataFrame(proof_spy)
        return_list = [gdp, proof, proof_spy]
        return gdp, proof, proof_spy





class Proof_of_Concept2(object):

    def __init__(self, report_date):
        self.report_date = str(report_date)[:10]
        self.saveMonth = self.report_date[:7]
        self.saveDay = str(datetime.now())[8:10]
        self.saveRec = Path(f"data/recommenders/{self.saveMonth}/{self.report_date}/")
        self.saveReport = Path(f"reports/portfolio/{self.saveMonth}/{self.report_date}/")
        self.file_loc = self.saveRec / f"recommender_final_return_dataFrame.pkl"
        self.portfolio_file_est = self.saveReport / f"roll_out_list_a.pkl"


    def setup(self, portfolio_file, initial_cash=5000):
        portfolio_file.reset_index()
        divisor = len(portfolio_file["symbol"])
        proof = pd.DataFrame(portfolio_file[["symbol", "allocation"]]).sort_values("symbol")
        start_0 = proof["allocation"].sum() / 100
        self.initial_cash = int(float(initial_cash) * start_0)

        c = yf.download(list(proof["symbol"]), start=self.report_date)["Adj Close"]
        b = []
        for i in proof["symbol"]:
            b.append(company_longName(i))

        proof["companyName"] = b
        proof["start_price"] = list(c.iloc[0])
        proof["current_price"] = list(c.iloc[-1])
        proof = proof.dropna()
        proof["initial_investment"] = self.initial_cash * (proof["allocation"] / 100)
        proof["shares"] = round(proof["initial_investment"] / proof["start_price"], 2)
        proof["cash_now"] = round(proof["shares"] * proof["current_price"], 2)
        proof["return"] = round(
            (
                (proof["cash_now"] - proof["initial_investment"])
                / proof["initial_investment"]
            )
            * 100,
            2,
        )
        proof = proof.sort_values("return", ascending=False)
        proof["rank"] = range(1, len(proof["symbol"]) + 1)
        proof = proof.set_index("rank")

        fd = yf.download("SPY", start=self.report_date)
        og_price = round(fd["Adj Close"][0], 2)
        new_price = round(fd["Adj Close"][-1], 2)
        proof_spy = pd.DataFrame(["SPY"], columns=["SPY"])
        proof_spy["start_price"] = og_price
        proof_spy["current_price"] = new_price
        proof_spy["initial_investment"] = round(
            self.initial_cash / len(proof_spy["SPY"]), 2
        )
        proof_spy["shares"] = round(
            proof_spy["initial_investment"] / proof_spy["start_price"], 2
        )
        proof_spy["cash_now"] = round(
            proof_spy["shares"] * proof_spy["current_price"], 2
        )
        proof_spy["return"] = round(
            (
                (proof_spy["cash_now"] - proof_spy["initial_investment"])
                / proof_spy["initial_investment"]
            )
            * 100,
            2,
        )

        beat_num = proof_spy["return"][0]
        proof_2 = proof[proof["return"] > 0.0]
        proof_3 = proof[proof["return"] > beat_num]

        winning_percentage = round((len(proof_2["symbol"]) / divisor) * 100, 2)
        beat_spy_percentage = round((len(proof_3["symbol"]) / divisor) * 100, 2)
        act_ror = round(
            (
                (proof["cash_now"].sum() - proof["initial_investment"].sum())
                / proof["initial_investment"].sum()) * 100, 2,)

        gdp = pd.DataFrame(
            ["Recommended Stocks", "SPY Index"], columns=["strategy_vs_benchmark"]
        )
        gdp["starting_money"] = [
            f"${proof['initial_investment'].sum()}",
            f"${proof_spy['initial_investment'].sum()}",
        ]
        gdp["ending_money"] = [
            f"${proof['cash_now'].sum()}",
            f"${proof['cash_now'].sum()}",
        ]
        gdp["return"] = [
            f"{round(act_ror,2)}%",
            f"{round(float(proof_spy['return']),2)}%",
        ]

        gdp = gdp.set_index("strategy_vs_benchmark")
        if exists(self.saveRec / f"recommender_final_return_dataFrame.pkl"):
            self.dff = pd.read_pickle(self.saveRec / f"recommender_final_return_dataFrame.pkl")
        else:
            self.dff = pd.read_csv(self.saveRec / f"recommender_final_return_dataFrame.csv")

        st.caption(f"{'__'*25}\n{'__'*25}")
        st.header(f"> __The Facts: [MIN VOLATILITY]__")
        st.write(f" - Start Position [{self.report_date}] ")
        st.write(f" - Today's Position [{str(datetime.now())[:10]}] ")
        st.table(gdp)

        st.subheader(f"* __Proof returns__")
        st.write(f" - equally weighted portfolio")
        st.write(
            f" - Winning Stock Picks [Positive Return] = \
                {len(proof_2['symbol'])}/{divisor}, [{winning_percentage}%] ")
        st.write(
            f" - Stocks Outperforming The SPY  = \
                {len(proof_3['symbol'])}/{divisor}, [{beat_spy_percentage}%   ]]")
        st.subheader(
            f"* __Initial Portfolio Optimization Modeled On {self.report_date}__")


        if exists(self.saveReport / "roll_out_list_a.pkl"): 
            zzz = pd.DataFrame(pd.read_pickle(self.saveReport / "roll_out_list_a.pkl")).reset_index()
            zzz.columns = ["A", "B"]
            lst = list(zzz["B"])
            lst_a = lst[:4]
            lst_b = lst[5:9]
            for i in lst_a[1:]:
                st.write(f" - {i}")                
        else:
            zzz = pd.DataFrame(pd.read_csv(self.saveReport / "roll_out_list_a.csv")).reset_index()
            zzz.columns = ["A", "B"]
            lst = list(zzz["B"])
            lst_a = lst[:4]
            lst_b = lst[5:9]
            for i in lst_a[1:]:
                st.write(f" - {i}")           

        st.table(proof)
        st.caption(f"{'__'*25}\n{'__'*25}")
        gdp = pd.DataFrame(gdp)
        proof = pd.DataFrame(proof)
        return_list = [gdp, proof]
        return gdp, proof





class Proof_of_Concept3(object):

    def __init__(self, report_date):
        self.report_date = str(report_date)[:10]
        self.saveMonth = self.report_date[:7]
        self.saveDay = str(datetime.now())[8:10]
        self.saveRec = Path(f"data/recommenders/{self.saveMonth}/{self.report_date}/")
        self.saveReport = Path(f"reports/portfolio/{self.saveMonth}/{self.report_date}/")
        self.file_loc = self.saveRec / f"recommender_final_return_dataFrame.pkl"
        self.portfolio_file_est = self.saveReport / f"roll_out_list_a.pkl"


    def setup(self, portfolio_file, initial_cash=5000):
        portfolio_file.reset_index()
        divisor = len(portfolio_file["symbol"])
        proof = pd.DataFrame(portfolio_file[["symbol", "allocation"]]).sort_values("symbol")

        start_0 = proof["allocation"].sum() / 100
        self.initial_cash = int(float(initial_cash) * start_0)

        c = yf.download(list(proof["symbol"]), start=self.report_date)["Adj Close"]
        b = []
        for i in proof["symbol"]:
            b.append(company_longName(i))

        proof["companyName"] = b
        proof["start_price"] = list(c.iloc[0])
        proof["current_price"] = list(c.iloc[-1])
        proof = proof.dropna()
        proof["initial_investment"] = self.initial_cash * (proof["allocation"] / 100)
        proof["shares"] = round(proof["initial_investment"] / proof["start_price"], 2)
        proof["cash_now"] = round(proof["shares"] * proof["current_price"], 2)
        proof["return"] = round(
            (
                (proof["cash_now"] - proof["initial_investment"])
                / proof["initial_investment"]
            )\
                 * 100, 2, 
        )
        proof = proof.sort_values("return", ascending=False)
        proof["rank"] = range(1, len(proof["symbol"]) + 1)
        proof = proof.set_index("rank")

        fd = yf.download("SPY", start=self.report_date)
        og_price = round(fd["Adj Close"][0], 2)
        new_price = round(fd["Adj Close"][-1], 2)
        proof_spy = pd.DataFrame(["SPY"], columns=["SPY"])
        proof_spy["start_price"] = og_price
        proof_spy["current_price"] = new_price
        proof_spy["initial_investment"] = round(
            self.initial_cash / len(proof_spy["SPY"]), 2
        )
        proof_spy["shares"] = round(
            proof_spy["initial_investment"] / proof_spy["start_price"], 2
        )
        proof_spy["cash_now"] = round(
            proof_spy["shares"] * proof_spy["current_price"], 2
        )
        proof_spy["return"] = round(
            (
                (proof_spy["cash_now"] - proof_spy["initial_investment"])
                / proof_spy["initial_investment"]
            )
            * 100,
            2,
        )

        beat_num = proof_spy["return"][0]
        proof_2 = proof[proof["return"] > 0.0]
        proof_3 = proof[proof["return"] > beat_num]

        winning_percentage = round((len(proof_2["symbol"]) / divisor) * 100, 2)
        beat_spy_percentage = round((len(proof_3["symbol"]) / divisor) * 100, 2)
        act_ror = round(
            (
                (proof["cash_now"].sum() - proof["initial_investment"].sum())
                / proof["initial_investment"].sum()
            )* 100, 2,
        )

        gdp = pd.DataFrame(["Recommended Stocks", "SPY Index"], columns=["strategy_vs_benchmark"])
        gdp["starting_money"] = [
            f"${proof['initial_investment'].sum()}",
            f"${proof_spy['initial_investment'].sum()}",
        ]
        gdp["ending_money"] = [
            f"${proof['cash_now'].sum()}",
            f"${proof['cash_now'].sum()}",
        ]
        gdp["return"] = [
            f"{round(act_ror,2)}%",
            f"{round(float(proof_spy['return']),2)}%",
        ]
        gdp = gdp.set_index("strategy_vs_benchmark")


        if exists(self.saveReport / f"roll_out_list_c.pkl"):
            self.dff = pd.read_pickle(self.saveReport / f"roll_out_list_c.pkl")
        else:
            self.dff = pd.read_csv(self.saveReport / f"roll_out_list_c.csv")


        st.caption(f"{'__'*25}\n{'__'*25}")
        st.header(f"> __The Facts: [SHARPE NEAR-EQUAL WTS]__")
        st.write(f" - Start Position [{self.report_date}] ")
        st.write(f" - Today's Position [{str(datetime.now())[:10]}] ")
        st.table(gdp)

        st.subheader(f"* __Proof returns__")
        st.write(f" - equally weighted portfolio")
        st.write(f" - Winning Stock Picks [Positive Return] = {len(proof_2['symbol'])}/{divisor}, [{winning_percentage}%] ")
        st.write(f" - Stocks Outperforming The SPY  = {len(proof_3['symbol'])}/{divisor}, [{beat_spy_percentage}%   ]]")
        st.subheader(f"* __Initial Portfolio Optimization Modeled On {self.report_date}__")


        if exists(self.saveReport / "roll_out_list_a.pkl"): 
            zzz = pd.DataFrame(pd.read_pickle(self.saveReport / "roll_out_list_a.pkl")).reset_index()
            zzz.columns = ["A", "B"]
            lst = list(zzz["B"])
            lst_a = lst[:4]
            lst_b = lst[5:9]
            for i in lst_a[1:]:
                st.write(f" - {i}")                
        else:
            zzz = pd.DataFrame(pd.read_csv(self.saveReport / "roll_out_list_a.csv")).reset_index()
            zzz.columns = ["A", "B"]
            lst = list(zzz["B"])
            lst_a = lst[:4]
            lst_b = lst[5:9]
            for i in lst_a[1:]:
                st.write(f" - {i}")

        st.table(proof)
        st.caption(f"{'__'*25}\n{'__'*25}")
        gdp = pd.DataFrame(gdp)
        proof = pd.DataFrame(proof)
        return_list = [gdp, proof]
        return gdp, proof





class Proof_of_Concept4(object):
    def __init__(self, report_date):
        self.report_date = str(report_date)[:10]
        self.saveMonth = self.report_date[:7]
        self.saveDay = str(datetime.now())[8:10]
        self.saveRec = Path(f"data/recommenders/{self.saveMonth}/{self.report_date}/")
        self.saveReport = Path(f"reports/portfolio/{self.saveMonth}/{self.report_date}/")
        self.file_loc = self.saveRec / f"recommender_final_return_dataFrame.pkl"
        self.portfolio_file_est = self.saveReport / f"roll_out_list_a.pkl"


    def setup(self, portfolio_file, initial_cash=5000):
        portfolio_file.reset_index()
        divisor = len(portfolio_file["symbol"])
        proof = pd.DataFrame(portfolio_file["symbol"]).sort_values("symbol")
        self.initial_cash = initial_cash
        c = yf.download(list(proof["symbol"]), start=self.report_date)["Adj Close"]
        b = []
        for i in proof["symbol"]:
            b.append(company_longName(i))

        
        proof["allocation"] = round(100 / len(proof["symbol"]), 2)
        proof["companyName"] = b
        proof["start_price"] = list(c.iloc[0])
        proof["current_price"] = list(c.iloc[-1])
        proof = proof.dropna()
        proof["initial_investment"] = self.initial_cash * (proof["allocation"] / 100)
        proof["shares"] = round(proof["initial_investment"] / proof["start_price"], 2)
        proof["cash_now"] = round(proof["shares"] * proof["current_price"], 2)
        proof["return"] = round(
            (
                (proof["cash_now"] - proof["initial_investment"])
                / proof["initial_investment"]
            )
            * 100,
            2,
        )
        
        proof = proof.sort_values("return", ascending=False)
        proof["rank"] = range(1, len(proof["symbol"]) + 1)
        proof = proof.set_index("rank")

        fd = yf.download("SPY", start=self.report_date)
        og_price = round(fd["Adj Close"][0], 2)
        new_price = round(fd["Adj Close"][-1], 2)
        proof_spy = pd.DataFrame(["SPY"], columns=["SPY"])
        proof_spy["start_price"] = og_price
        proof_spy["current_price"] = new_price
        proof_spy["initial_investment"] = round(
            self.initial_cash / len(proof_spy["SPY"]), 2
        )
        proof_spy["shares"] = round(
            proof_spy["initial_investment"] / proof_spy["start_price"], 2
        )
        proof_spy["cash_now"] = round(
            proof_spy["shares"] * proof_spy["current_price"], 2
        )
        proof_spy["return"] = round(
            (
                (proof_spy["cash_now"] - proof_spy["initial_investment"])
                / proof_spy["initial_investment"]
            )
            * 100,
            2,
        )

        beat_num = proof_spy["return"][0]
        proof_2 = proof[proof["return"] > 0.0]
        proof_3 = proof_2[proof_2["return"] > beat_num]

        winning_percentage = round((len(proof_2["symbol"]) / divisor) * 100, 2)
        beat_spy_percentage = round((len(proof_3["symbol"]) / divisor) * 100, 2)
        act_ror = round(
            (
                (proof["cash_now"].sum() - proof["initial_investment"].sum())
                / proof["initial_investment"].sum()
            )
            * 100, 2,
        )

        gdp = pd.DataFrame(["Recommended Stocks", "SPY Index"], columns=["strategy_vs_benchmark"])
        gdp["starting_money"] = [f"${proof['initial_investment'].sum()}", f"${proof_spy['initial_investment'].sum()}"]
        gdp["ending_money"] = [f"${proof['cash_now'].sum()}",f"${proof['cash_now'].sum()}",]
        gdp["return"] = [f"{round(act_ror,2)}%",f"{round(float(proof_spy['return']),2)}%",]
        gdp = gdp.set_index("strategy_vs_benchmark")


        if exists(self.saveReport / f"roll_out_list_c.pkl"):
            self.dff = pd.read_pickle(self.saveReport / f"roll_out_list_c.pkl")
        else:
            self.dff = pd.read_csv(self.saveReport / f"roll_out_list_c.csv")        


        st.caption(f"{'__'*25}\n{'__'*25}")
        st.header(f"> __The Facts: [EQUALLY WEIGHTED]__")
        st.write(f" - Start Position [{self.report_date}] ")
        st.write(f" - Today's Position [{str(datetime.now())[:10]}] ")
        st.table(gdp)

        st.subheader(f"* __Proof returns__")
        st.write(f" - equally weighted portfolio")
        st.write(f" - Winning Stock Picks [Positive Return] = {len(proof_2['symbol'])}/{divisor}, [{winning_percentage}%] ")
        st.write(f" - Stocks Outperforming The SPY  = {len(proof_3['symbol'])}/{divisor}, [{beat_spy_percentage}%   ]]")
        st.subheader(f"* __Initial Portfolio Optimization Modeled On {self.report_date}__")

        if exists(self.saveReport / "roll_out_list_a.pkl"): 
            zzz = pd.DataFrame(pd.read_pickle(self.saveReport / "roll_out_list_a.pkl")).reset_index()
            zzz.columns = ["A", "B"]
            lst = list(zzz["B"])
            lst_a = lst[:4]
            lst_b = lst[5:9]
            for i in lst_a[1:]:
                st.write(f" - {i}")                
        else:
            zzz = pd.DataFrame(pd.read_csv(self.saveReport / "roll_out_list_a.csv")).reset_index()
            zzz.columns = ["A", "B"]
            lst = list(zzz["B"])
            lst_a = lst[:4]
            lst_b = lst[5:9]
            for i in lst_a[1:]:
                st.write(f" - {i}")

        st.table(proof)
        st.caption(f"{'__'*25}\n{'__'*25}")

        st.subheader(f"** > Final Results From ({self.report_date}) **")
        st.write(f" - total stocks = {len(self.dff.index)}")
        # st.table(self.dff)

        gdp = pd.DataFrame(gdp)
        proof = pd.DataFrame(proof)
        return_list = [gdp, proof]
        return gdp, proof





class Proof_of_Concept_MCC(object):

    def __init__(self, report_date):
        self.report_date = str(report_date)[:10]
        self.saveMonth = self.report_date[:7]
        self.saveDay = str(datetime.now())[8:10]
        self.saveRec = Path(f"data/recommenders/{self.saveMonth}/{self.report_date}/")
        self.saveReport = Path(f"reports/portfolio/{self.saveMonth}/{self.report_date}/")
        self.file_loc = self.saveRec / f"recommender_final_return_dataFrame.pkl"
        self.portfolio_file_est = self.saveReport / f"roll_out_list_a.pkl"


    def setup(self, portfolio_file, initial_cash=5000):
        portfolio_file.reset_index()
        divisor=len(portfolio_file['symbol'])
        proof = pd.DataFrame(portfolio_file[["ticker", "Weight"]]).sort_values("ticker")
        proof.columns = ["symbol", "allocation"]
        start_0 = proof["allocation"].sum() / 100
        self.initial_cash = int(float(initial_cash) * start_0)

        c = yf.download(list(proof["symbol"]), start=self.report_date)["Adj Close"]
        b = []
        for i in proof["symbol"]:
            b.append(company_longName(i))

        proof["companyName"] = b
        proof["start_price"] = list(c.iloc[0])
        proof["current_price"] = list(c.iloc[-1])
        proof = proof.dropna()
        proof["initial_investment"] = self.initial_cash * (proof["allocation"] / 100)
        proof["shares"] = round(proof["initial_investment"] / proof["start_price"], 2)
        proof["cash_now"] = round(proof["shares"] * proof["current_price"], 2)
        proof["return"] = round(
            (
                (proof["cash_now"] - proof["initial_investment"])
                / proof["initial_investment"]
            )
            * 100,
            2,
        )
        proof = proof.sort_values("return", ascending=False)
        proof["rank"] = range(1, len(proof["symbol"]) + 1)
        proof = proof.set_index("rank")

        fd = yf.download("SPY", start=self.report_date)
        og_price = round(fd["Adj Close"][0], 2)
        new_price = round(fd["Adj Close"][-1], 2)
        proof_spy = pd.DataFrame(["SPY"], columns=["SPY"])
        proof_spy["start_price"] = og_price
        proof_spy["current_price"] = new_price
        proof_spy["initial_investment"] = round(
            self.initial_cash / len(proof_spy["SPY"]), 2
        )
        proof_spy["shares"] = round(
            proof_spy["initial_investment"] / proof_spy["start_price"], 2
        )
        proof_spy["cash_now"] = round(
            proof_spy["shares"] * proof_spy["current_price"], 2
        )
        proof_spy["return"] = round(
            (
                (proof_spy["cash_now"] - proof_spy["initial_investment"])
                / proof_spy["initial_investment"]
            )
            * 100,
            2,
        )

        beat_num = proof_spy["return"][0]
        proof_2 = proof[proof["return"] > 0.0]
        proof_3 = proof[proof["return"] > beat_num]

        winning_percentage = round(
            (len(proof_2["symbol"]) / len(proof["symbol"])) * 100, 2
        )
        beat_spy_percentage = round(
            (len(proof_3["symbol"]) / len(proof["symbol"])) * 100, 2
        )
        act_ror = round(
            (
                (proof["cash_now"].sum() - proof["initial_investment"].sum())
                / proof["initial_investment"].sum()
            )
            * 100,
            2,
        )

        gdp = pd.DataFrame(
            ["Recommended Stocks", "SPY Index"], columns=["strategy_vs_benchmark"]
        )
        gdp["starting_money"] = [
            f"${proof['initial_investment'].sum()}",
            f"${proof_spy['initial_investment'].sum()}",
        ]
        gdp["ending_money"] = [
            f"${proof['cash_now'].sum()}",
            f"${proof['cash_now'].sum()}",
        ]
        gdp["return"] = [
            f"{round(act_ror,2)}%",
            f"{round(float(proof_spy['return']),2)}%",
        ]
        gdp = gdp.set_index("strategy_vs_benchmark")
        self.dff = pd.read_pickle(self.file_loc)

        st.caption(f"{'__'*25}\n{'__'*25}")
        st.header(f"> __The Facts: [MONTE CARLO CHOLESKY PORTFOLIO]__")
        st.write(f" - Start Position [{self.report_date}] ")
        st.write(f" - Today's Position [{str(datetime.now())[:10]}] ")
        st.table(gdp)

        st.subheader(f"* __Proof returns__")
        st.write(f" - equally weighted portfolio")
        st.write(
            f" - Winning Stock Picks [Positive Return] = {len(proof_2['symbol'])}/{divisor}, [{winning_percentage}%] "
        )
        st.write(
            f" - Stocks Outperforming The SPY  = {len(proof_3['symbol'])}/{divisor}, [{beat_spy_percentage}%   ]]"
        )
        st.subheader(
            f"* __Initial Portfolio Optimization Modeled On {self.report_date}__"
        )
        st.table(proof)
        st.caption(f"{'__'*25}\n{'__'*25}")
        return





# if __name__ == "__main__":
#     sdate = date(2021, 7, 15)  # start date
#     edate = date(2021, 8, 26)  # end date
#     date_range_lst = list(pd.date_range(sdate, edate - timedelta(days=1), freq="d"))
#     report_date = st.sidebar.date_input(
#         label="> recommender date:",
#         value=date(2021, 7, 15),
#         min_value=sdate,
#         max_value=edate,
#         key="date to run proof",
#         help="Select a date in the range between 2021.07.15 - 2021.08.26. \
#             This date will be the date the recommender model was run and we \
#                 will use the resulting tickers for our proof",
#     )

#     initial_investment = st.sidebar.number_input(label="enter Initial Investment Amount:", value=5000)
