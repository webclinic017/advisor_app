from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from src.tools import functions as f0
from src.tools import lists as l0
from src.tools import scripts as s0
from src.tools import widgets as w0

from pages.snapshot import Snapshot



class Home(object):


    def __init__(self, today_stamp):
        self.today_stamp = str(today_stamp)[:10]
        
        st.header("⬛ 𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄚𝄚𝄚 · Home · 𝄚𝄚𝄚𝄙𝄙𝄘𝄘𝄗𝄗𝄖𝄖 ⬛")
        st.header(f"{' '*25}")
        st.header(f"{'𝄗'*32}")        


    def run_home(self):
        
        # cols = st.columns(1)
        # with cols[0]:
        #     st.subheader("𝄖𝄗𝄘𝄙𝄚 Live Stock Screener Lists")
        #     screener = st.selectbox("", l0.names_of_screeners)
        #     if screener != "-":
        #         Snapshot(self.today_stamp).get_screener_display(screener)              
        # st.write(f"{'_'*25}")
        
        
        # cols = st.columns(1)
        # with cols[0]:
        #     st.subheader("𝄖𝄗𝄘𝄙𝄚 Google Trending Topics, Stocks, Assets, & More")
        #     if st.button("Source Trending"):
        #         Snapshot(self.today_stamp).run_trending()    
        # st.write(f"{'_'*25}")
              
                
        # cols = st.columns(1)
        # with cols[0]:
        #     st.subheader("𝄖𝄗𝄘𝄙𝄚 Multivariate Market Analysis")       
        #     if st.button("Source Multivariate"):
        #         Snapshot(self.today_stamp).run_multivariate()  
        # st.write(f"{'_'*25}")



        my_expander = st.expander("𝄖𝄖𝄗𝄗𝄗𝄘𝄘𝄘𝄘𝄙𝄙𝄙𝄙𝄙 Disclosures 𝄙𝄙𝄙𝄙𝄙𝄘𝄘𝄘𝄘𝄗𝄗𝄗𝄖𝄖", expanded=False)
        with my_expander:
            clicked = w0.home_disclosure()
