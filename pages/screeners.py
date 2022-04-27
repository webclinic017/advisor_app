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
        
        st.header("⬛ 𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄚𝄚𝄚 · Screener · 𝄚𝄚𝄚𝄙𝄙𝄘𝄘𝄗𝄗𝄖𝄖 ⬛")
        st.header(f"{'𝄗'*33}") # 𝄗 𝄖


    def run_screen(self):
        
        cols = st.columns(2)
        with cols[0]:
            st.subheader("𝄖𝄗𝄘𝄙𝄚 Live Stock Screener Lists")
            screener = st.selectbox("", l0.names_of_screeners)
            if screener != "-":
                Snapshot(self.today_stamp).get_screener_display(screener)              
        st.write(f"{'_'*10}")        

        cols = st.columns(1)
        with cols[0]:
            st.subheader("𝄖𝄗𝄘𝄙𝄚 Google Trending Topics, Stocks, Assets, & More")
            if st.button("Source Trending"):
                Snapshot(self.today_stamp).run_trending()    
        st.write(f"{'_'*25}")
                
        cols = st.columns(1)
        with cols[0]:
            st.subheader("𝄖𝄗𝄘𝄙𝄚 Multivariate Market Analysis")       
            if st.button("Source Multivariate"):
                Snapshot(self.today_stamp).run_multivariate()  
