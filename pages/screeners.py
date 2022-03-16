import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from datetime import datetime

from src.tools import functions as f0
from src.tools import lists as l0
from src.tools import scripts as s0
from src.tools import widgets as w0
from pages.snapshot import Snapshot

plt.style.use("ggplot")
plt.rcParams["axes.facecolor"] = "silver"


class Screeners(object):


    def __init__(self, today_stamp):
        self.today_stamp = str(today_stamp)[:10]
        self.stage_lst = l0.general_pages
        self.major_indicies = l0.major_indicies
        self.major_index_names = l0.major_index_names


    def run_screen(self):
        st.header("[Screener]")
        st.write("- Select Top Screeners For Live Market Updates")
        screener = st.selectbox("", l0.names_of_screeners)
        if st.button("Source Screeners"):
            Snapshot(self.today_stamp).get_screener_display(screener)
        st.write(f"{'_'*25}")


        st.subheader("Multivariate")
        st.write("- Recurrent Neural Network [RNN] Analysis")
        st.write("- Consumer Sentiment vs Industrial Production")
        if st.button("Source Multivariate"):
            Snapshot(self.today_stamp).run_multivariate()  
        st.write(f"{'_'*25}")


        st.subheader("Trending")
        st.write(" - Google Trending Topics, Stocks, Assets, & More")
        if st.button("Source Trending"):
            Snapshot(self.today_stamp).run_trending()
        st.write(f"{'_'*25}")
