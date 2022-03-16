import pandas as pd
from os.path import exists
from finvizfinance.quote import finvizfinance
from datetime import datetime
from pathlib import Path

from src.tools import functions as f0



class Recommendations5(object):
    def __init__(self, today_stamp):
        self.today_stamp = today_stamp
        self.saveMonth = str(datetime.now())[:7]
        self.saveDay = str(datetime.now())[8:10]

        self.saveRec = Path(f"data/recommenders/{self.saveMonth}/{self.today_stamp}/")
        if not self.saveRec.exists():
            self.saveRec.mkdir(parents=True)



    def stage_V(self):
        if exists(self.saveRec / "recommender_final_return_dataFrame.pkl"):
            return
        else:
            fd = pd.read_pickle(self.saveRec / "recommender_04_return_dataFrame.pkl")
            df = pd.DataFrame(fd).reset_index()
            df = df[df["my_score"] > 39.99]
            cde = pd.DataFrame(df).set_index(["rank", "my_score"])
            cde.to_pickle(self.saveRec / "recommender_final_return_dataFrame.pkl")
            return