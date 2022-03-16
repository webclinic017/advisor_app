from datetime import datetime
from pathlib import Path
from re import L
import pandas as pd
from os.path import exists

import pages as p1
from src import gmail as g1
from src import data as d1
from src.models.portfolio.proof_port import The_Portfolio_Optimizer
from src.models.recommender.recommender_stage_00 import Recommendations0 as r0
from src.models.recommender.recommender_stage_01 import Recommendations1 as r1
from src.models.recommender.recommender_stage_02 import Recommendations2 as r2
from src.models.recommender.recommender_stage_03 import Recommendations3 as r3
from src.models.recommender.recommender_stage_04 import Recommendations4 as r4
from src.models.recommender.recommender_stage_05 import Recommendations5 as r5
from src.models.portfolio.proof import (
    Proof_of_Concept,
    Proof_of_Concept2,
    # Proof_of_Concept3,
    Proof_of_Concept4,
    Proof_of_Concept_000,
)


class Builder(object):

    def __init__(self, today):
        self.w0 = f"\n  {' *'*34} \n\n * * * BUILD STAGE"
        self.w1 = f" * * * \n\n  {' *'*34} \n"

        self.today_stamp = today
        self.saveMonth = str(today)[:7]


    def build_stage_0(self):
        if exists(
            f"data/recommenders/{self.saveMonth}/{self.today_stamp}/recommender_00_return_dataFrame.pkl"
        ):
            print(
                f"{self.w0} (0) - Compile Screeners & Stock List - [COMPLETE] {self.w1}"
            )
            return
        else:
            d1.Source_Data(self.today_stamp).save_screeners_and_tickers()
            r0(self.today_stamp).data_source()
            print(
                f"{self.w0} (0) - Compile Screeners & Stock List - [COMPLETE] {self.w1}"
            )


    def build_stage_1(self):
        r1(self.today_stamp).run_rec1()
        print(f"{self.w0} (1) - Analyst's Score - [COMPLETE] {self.w1}")


    def build_stage_2(self):
        r2(self.today_stamp).run_rec2()
        print(f"{self.w0} (2) - Technical Analysis - [COMPLETE] {self.w1}")


    def build_stage_3(self):
        r3(self.today_stamp).run_rec3()
        print(
            "\n* * * * * * * Recommender Stage 3 [Sentiment Analysis] Done * * * * * * * \n"
        )


    def build_stage_4(self):
        p1.Recommender(self.today_stamp).create_final()
        print(
            "\n* * * * * * * Recommender Stage 4 [Compiler - My Score] Done * * * * * * * \n"
        )


    def build_stage_5(self):
        p1.Recommender(self.today_stamp).stage_V()
        print("\n* * * * * * * Recommender Stage 5 [Final Trim] Done * * * * * * * \n")


    def build_stage_6(self):
        if exists(
            f"reports/portfolio/{self.saveMonth}/{self.today_stamp}/max_sharpe_df_1.pkl"
        ):
            print(
                "\n* * * * * * * [X] COMPLETE - Recommender Stage 6 [Portfolio Construction] * * * * * * * \n"
            )
            return
        else:
            The_Portfolio_Optimizer(39, self.today_stamp).optimize(5000, 25000, 17)
            print(
                "\n* * * * * * * [X] COMPLETE - Recommender Stage 6 [Portfolio Construction] * * * * * * * \n"
            )
            return


    def build_stage_7(self, initial_cash=5000):
        saveReport_A = Path(f"reports/portfolio/{saveMonth}/{stamp}/")
        max_sharpe_df_3 = pd.read_pickle(saveReport_A / f"max_sharpe_df_3.pkl")
        min_vol_df_3 = pd.read_pickle(saveReport_A / f"min_vol_df_3.pkl")
        max_sharpe_df_1 = pd.read_pickle(saveReport_A / f"max_sharpe_df_1.pkl")
        edate = self.today_stamp[:-2] + str(int(self.today_stamp[-2:]) + 1)

        loc_file = Path(f"reports/port_results/{self.saveMonth}/{self.today_stamp}")
        if not loc_file.exists():
            loc_file.mkdir(parents=True)


        if exists(
            f"reports/port_results/{self.saveMonth}/{self.today_stamp}/maximum_sharpe_ratio_best.csv"
        ):
            print(
                "\n* * * * * * * * * * [X] COMPLETE - Recommender Stage 7 [Proof - A] * * * * * * * * * * \n"
            )
        else:
            Proof_of_Concept(self.today_stamp).setup(
                max_sharpe_df_3, initial_cash
            )
            print(
                "\n* * * * * * * * * * [X] COMPLETE - Recommender Stage 7 [Proof - A] * * * * * * * * * * \n"
            )


        if exists(
            f"reports/port_results/{self.saveMonth}/{self.today_stamp}/minimum_volatility_portfolio_best.csv"
        ):
            print(
                "\n* * * * * * * * * * [X] COMPLETE - Recommender Stage 7 [Proof - B] * * * * * * * * * * \n"
            )
        else:
            Proof_of_Concept2(self.today_stamp).setup(
                min_vol_df_3, initial_cash
            )
            print(
                "\n* * * * * * * * * * [X] COMPLETE - Recommender Stage 7 [Proof - B] * * * * * * * * * * \n"
            )


        # if exists(f"reports/port_results/{self.saveMonth}/{self.today_stamp}/maximum_sharpe_ratio_portfolio_random.csv"):
        #     print("\n* * * * * * * * * * [X] COMPLETE - Recommender Stage 7 [Proof - C] * * * * * * * * * * \n")

        # else:
        #     return_lst = Proof_of_Concept3(self.today_stamp).setup(max_sharpe_df_1, initial_cash)
        #     return_lst[0].to_csv(loc_file / f"maximum_sharpe_ratio_portfolio_random-VS-sp500.csv")
        #     return_lst[1].to_csv(loc_file / f"maximum_sharpe_ratio_portfolio_random.csv")
        #     return_lst[1].to_csv(loc_file / f"proof_c.csv")
        #     print("\n* * * * * * * * * * [X] COMPLETE - Recommender Stage 7 [Proof - C] * * * * * * * * * * \n")


        if exists(
            f"reports/port_results/{self.saveMonth}/{self.today_stamp}/maximum_sharpe_ratio_portfolio_equalWT.csv"
        ):
            print(
                "\n* * * * * * * * * * [X] COMPLETE - Recommender Stage 7 [Proof - D] * * * * * * * * * * \n"
            )
        else:
            Proof_of_Concept4(self.today_stamp).setup(
                max_sharpe_df_3, initial_cash
            )
            print(
                "\n* * * * * * * * * * [X] COMPLETE - Recommender Stage 7 [Proof - D] * * * * * * * * * * \n"
            )


        if exists(
            f"reports/port_results/{self.saveMonth}/{self.today_stamp}/monte_carlo_cholesky.csv"
        ):
            print(
                "\n* * * * * * * * * * [X] COMPLETE - Recommender Stage 7 [Proof - MCC] * * * * * * * * * * \n"
            )
        else:
            Proof_of_Concept_000(self.today_stamp).setup(
                max_sharpe_df_3, initial_cash
            )
            print(
                "\n* * * * * * * * * * [X] COMPLETE - Recommender Stage 7 [Proof - MCC] * * * * * * * * * * \n"
            )
            return
        return


    def build_stage_8(self):
        g1.The_Only_Mailer(self.today_stamp).mail_em_out()
        print(
            "\n * * * * * * * [X] COMPLETE - Recommender Stage 8 [EMAILER] * * * * * * * \n"
        )


if __name__ == "__main__":

    # stamp = "2021-07-14"
    stamp = str(datetime.now())[:10]

    saveMonth = stamp[:7]
    initial_investment = 5000

    b = Builder(stamp)
    b.build_stage_0()
    b.build_stage_1()
    b.build_stage_2()
    b.build_stage_3()
    b.build_stage_4()
    b.build_stage_5()
    b.build_stage_6()
    b.build_stage_7()
    b.build_stage_8()

    # self.saveRec = Path(f"data/recommenders/{self.saveMonth}/{self.today_stamp}/")
    # if not self.saveRec.exists():
    #     self.saveRec.mkdir(parents=True)

    # self.saveRaw = Path(f"data/raw/{self.saveMonth}/{self.today_stamp}/")
    # if not self.saveRaw.exists():
    #     self.saveRaw.mkdir(parents=True)

    # self.saveScreeners = Path(f"data/screeners/{self.saveMonth}/{self.today_stamp}/")
    # if not self.saveScreeners.exists():
    #     self.saveScreeners.mkdir(parents=True)

    # self.saveTickers = Path(f"data/tickers/{self.saveMonth}/{self.today_stamp}/")
    # if not self.saveTickers.exists():
    #     self.saveTickers.mkdir(parents=True)
