import pandas as pd
import finviz
from finvizfinance.quote import finvizfinance
from finviz import get_analyst_price_targets, get_news, get_stock
import streamlit as st

import src.tools.functions as f0



class Single_Asset_Analysis(object):


    def __init__(self):
        self.ticker = st.sidebar.text_input(label='[3] Enter Stock', value='AAPL')


    def run(self):

        st.sidebar.write('*'*25)
        if st.sidebar.button('Run'):
            stock = finvizfinance(self.ticker)
            stock_description = stock.TickerDescription()
            outer_ratings_df = stock.TickerOuterRatings()
            inside_trader_df = stock.TickerInsideTrader()

            company_name = f0.company_longName(self.ticker)
            x = f"{company_name} [{self.ticker}]"
    
            st.subheader(f"𝄖𝄖𝄗𝄗𝄘𝄘𝄙𝄙𝄙 Asset Overview · {x} 𝄙𝄙𝄙𝄘𝄘𝄗𝄗𝄖𝄖")
            st.write('*'*25)
            
            st.subheader('𝄖𝄗𝄘𝄙 Description')
            st.caption(stock_description)
            st.write(' '*25)
            # st.write('*'*25)

            st.subheader('𝄖𝄗𝄘𝄙 Stock Information')
            st.dataframe(pd.DataFrame.from_dict(get_stock('AAPL'), orient='index'))
            st.write(' '*25)
            # st.write('*'*25)
            
            st.subheader('𝄖𝄗𝄘𝄙 Stock Chart')
            st.image(stock.TickerCharts(out_dir='/home/gdp/Documents/library/portfolio/advisor_app/data/images/charts'))
            st.write(' '*25)
            # st.write('*'*25)

            st.subheader('𝄖𝄗𝄘𝄙 Analyst Ratings')
            st.dataframe(outer_ratings_df.head().set_index('Date'))
            st.write(' '*25)
            # st.write('*'*25)

            st.subheader('𝄖𝄗𝄘𝄙 Stock News')
            x = pd.DataFrame(get_news(self.ticker))
            x.columns=['date','headline','link','source']
            st.dataframe(x.set_index('date')    )
            st.write(' '*25)
            # st.write('*'*25)

            st.subheader('𝄖𝄗𝄘𝄙 Stock Insider Trading')
            st.dataframe(inside_trader_df.head())
            st.dataframe(pd.DataFrame.from_records(finviz.get_insider(self.ticker)))
            st.write(' '*25)
            # st.write('*'*25)

            st.subheader('𝄖𝄗𝄘𝄙 Stock Signals')
            st.dataframe(pd.DataFrame(get_analyst_price_targets(self.ticker)).set_index('date'))
