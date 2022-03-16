import pandas as pd
from yahooquery import Ticker
from os.path import exists
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pathlib import Path
from pathlib import Path
import streamlit as st
import yfinance as yf
import pickle5 as pickle 
import time
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go

from src.tools.functions import company_longName

pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)
pd.options.display.float_format = "{:,}".format

plt.style.use("ggplot")
sm, med, lg = "10", "15", "20"
plt.rcParams["font.size"] = sm  # controls default text sizes
plt.rc("axes", titlesize=med)  # fontsize of the axes title
plt.rc("axes", labelsize=med)  # fontsize of the x & y labels
plt.rc("xtick", labelsize=sm)  # fontsize of the tick labels
plt.rc("ytick", labelsize=sm)  # fontsize of the tick labels
plt.rc("legend", fontsize=sm)  # legend fontsize
plt.rc("figure", titlesize=lg)  # fontsize of the figure title
plt.rc("axes", linewidth=2)  # linewidth of plot lines
plt.rcParams["figure.figsize"] = [20, 10]
plt.rcParams["figure.dpi"] = 100
plt.rcParams["axes.facecolor"] = "silver"





class Proof_of_Concept_Viewer(object):
    
    def __init__(self, today_stamp, initial_cash=2500, save_output=True, graphit=True):
        self.save_output = save_output
        self.graphit = graphit
        self.initial_cash = initial_cash
        self.day = int(str(today_stamp)[8:10])
        self.month = int(str(today_stamp)[5:7])
        self.year = int(str(today_stamp)[:4])
        self.today_stamp = datetime(self.year, self.month, self.day)
        self.og_day = str(self.today_stamp)[:10]
        self.saveMonth = str(today_stamp)[:7]
        self.ender = str(datetime.now())[:10]
        self.saveRec = Path(f"data/recommenders/{str(self.today_stamp)[:4]}/{self.saveMonth}/{today_stamp}/")
        self.saveReport = Path(f"reports/portfolio/{self.saveMonth}/{today_stamp}/")
        
        self.final_loc = Path(f"reports/port_results/{self.saveMonth}/{today_stamp}/")
        if not self.final_loc.exists():
            self.final_loc.mkdir(parents=True)     
            
        self.saveAdvisor = Path(f"data/advisor/{self.saveMonth}/{today_stamp}/")
        if not self.saveAdvisor.exists():
            self.saveAdvisor.mkdir(parents=True)        

        self.saveProof = Path(f"data/proof/{today_stamp}/{self.ender}/")
        if not self.saveProof.exists():
            self.saveProof.mkdir(parents=True)

        self.spy = yf.download("^GSPC", start=self.today_stamp)


    def performance(self, portfolio_file, namer):
        og_wt = portfolio_file['allocation'].sum()
        new_wt_lst = []
        for i in portfolio_file['allocation']:
            new_wt_lst.append((i * 100) / og_wt)
        portfolio_file['allocation'] = (new_wt_lst)        
        self.portfolio_file = pd.DataFrame(portfolio_file)        
        
        divisor = len(self.portfolio_file["ticker"])
        total_allocation = self.portfolio_file["allocation"].sum() / 100
        self.port_tics = sorted(list(self.portfolio_file["ticker"]))
        self.today_stamp = datetime(self.year, self.month, self.day) + timedelta(days=1)
        self.namer = namer
        today_stamp = str(datetime.now())[:10]
        day = int(str(today_stamp)[8:10])
        month = int(str(today_stamp)[5:7])
        year = int(str(today_stamp)[:4])
        ender = datetime(year, month, day) - timedelta(days=1)     


        def section_proof_df():
            proof = pd.DataFrame(portfolio_file[["ticker", "allocation"]])
            proof = proof.sort_values("ticker")
            b = []
            for i in proof["ticker"]:
                b.append(company_longName(i))
            proof["companyName"] = b            
            
            df_close = pd.DataFrame(yf.download(self.port_tics, start=self.today_stamp, rounding=True)['Adj Close'])
            df_open = pd.DataFrame(yf.download(self.port_tics, start=self.today_stamp, rounding=True)['Open'])
            
            df_close = df_close.fillna(0.0)
            df_open = df_open.fillna(0.0)
            

            # df_close = pd.DataFrame()
            # df_open = pd.DataFrame()
            # hammerTime = Ticker(
            #     self.port_tics,
            #     asynchronous=True,
            #     formatted=False,
            #     backoff_factor=0.34,
            #     validate=True,
            #     verify=True,
            # )
            # hammer_hist = hammerTime.history(start=self.today_stamp).reset_index().set_index('date')
            # hammer_hist.index = pd.to_datetime(hammer_hist.index)
            # hammer_hist = hammer_hist.rename(columns={'symbol': 'ticker'})
            # for i in self.port_tics:
            #     try:
            #         z = pd.DataFrame(hammer_hist[hammer_hist['ticker'] == i]['adjclose'])
            #         df_close[i] = z
            #     except:
            #         print(f"failed ticker {i}")
            #         proof = proof.drop(proof[proof.ticker == i].index)
            #         self.port_tics.remove(i)
            # for i in self.port_tics:
            #     try:
            #         z = pd.DataFrame(hammer_hist[hammer_hist['ticker'] == i]['open'])
            #         df_open[i] = z
            #     except:
            #         print(f"failed ticker {i}")
            #         proof = proof.drop(proof[proof.ticker == i].index)
            #         self.port_tics.remove(i)
            
            
            try:
                proof['start_price'] = list(df_open.iloc[-1])
            except Exception:
                proof['start_price'] = list(df_close.iloc[0])
            proof["current_price"] = list(df_close.iloc[-1])            
            proof["initial_investment"] = round(self.initial_cash * (proof["allocation"] / 100), 2)
            proof["shares"] = round(proof["initial_investment"] / proof["start_price"], 2)
            proof["cash_now"] = round(proof["shares"] * proof["current_price"], 2)
            proof["return"] = round(((proof["cash_now"] - proof["initial_investment"]) / proof["initial_investment"]) * 100,2,)
            return proof, df_close


        def section_spy_df():
            og_price = round(self.spy["Adj Close"][0], 2)
            new_price = round(self.spy["Adj Close"][-1], 2)
            proof_spy = pd.DataFrame(["SPY"], columns=["SPY"])
            proof_spy["start_price"] = og_price
            proof_spy["current_price"] = new_price
            proof_spy["initial_investment"] = round(self.initial_cash / len(proof_spy["SPY"]), 2)
            proof_spy["shares"] = round(proof_spy["initial_investment"] / proof_spy["start_price"], 2)
            proof_spy["cash_now"] = round(proof_spy["shares"] * proof_spy["current_price"], 2)
            proof_spy["return"] = round(((proof_spy["cash_now"] - proof_spy["initial_investment"]) / proof_spy["initial_investment"])* 100,2,)
            beat_num = proof_spy["return"][0]
            proof_2 = proof[proof["return"] > 0.0]
            proof_3 = proof_2[proof_2["return"] > beat_num]
            winning_percentage = round((len(proof_2["ticker"]) / divisor) * 100, 2)
            beat_spy_percentage = round((len(proof_3["ticker"]) / divisor), 2)
            return proof_spy, winning_percentage, beat_spy_percentage, proof_2, proof_3               


        def section_one_df(df_close):
            one = pd.DataFrame(df_close.copy())
            shares = []
            allocation_lst = list(proof["allocation"])
            for k, v in enumerate(list(proof["ticker"])):
                shares.append(((allocation_lst[k] / 100) * self.initial_cash) / one[v].iloc[0])
            for k, v in enumerate(list(proof["ticker"])):
                one[v] = one[v] * shares[k]
            lst = list(proof["ticker"])
            one["portfolio"] = one[lst].sum(axis=1)          
            start_cash = round(proof["initial_investment"].sum(), 2)
            avg_1 = round(one["portfolio"].mean(), 2)
            high_1 = round(one["portfolio"].max(), 2)
            low_1 = round(one["portfolio"].min(), 2)
            mean_watermark = round(((avg_1 - start_cash) / start_cash) * 100, 2)
            high_watermark = round(((high_1 - start_cash) / start_cash) * 100, 2)
            low_watermark = round(((low_1 - start_cash) / start_cash) * 100, 2)
            mean_watermark_spy = round(proof_spy["return"].mean(), 2)
            high_watermark_spy = round(proof_spy["return"].max(), 2)
            low_watermark_spy = round(proof_spy["return"].min(), 2)
            x1 = one[one["portfolio"] == one["portfolio"].max()].index
            y1 = one["portfolio"].max()
            x2 = one[one["portfolio"] == one["portfolio"].min()].index
            y2 = one["portfolio"].min()
            for i in list(one["portfolio"]):
                if float(i) > high_1:
                    high_1 = float(i)
                else:
                    pass  
            one["since_open"] = round(((one["portfolio"] - start_cash) / start_cash) * 100, 2)
            act_ror = round(((list(one["portfolio"])[-1] - list(one["portfolio"])[0])/ list(one["portfolio"])[0])* 100,2,)
            gdp = pd.DataFrame(
                ["Recommended Stocks", "SPY Index"], 
                columns=["strategy_vs_benchmark"]
            )              
            gdp["starting_money"] = [
                f"${round(list(one['portfolio'])[0],2)}",
                f"${round(proof_spy['initial_investment'].sum(),2)}",
            ]
            gdp["ending_money"] = [
                f"${round(list(one['portfolio'])[-1],2)}",
                f"${round(proof_spy['cash_now'].sum(), 2)}",
            ]
            gdp["return"] = [
                f"{round(act_ror,2)}%",
                f"{round(float(proof_spy['return']),2)}%",
            ]
            gdp["mean_mark"] = [
                f"{mean_watermark}%",
                f"{mean_watermark_spy}%",
            ]        
            gdp["high_mark"] = [
                f"{high_watermark}%",
                f"{high_watermark_spy}%",
            ]
            gdp["low_mark"] = [
                f"{low_watermark}%",
                f"{low_watermark_spy}%",
            ]                        
            gdp = gdp.set_index("strategy_vs_benchmark")            
            return one, x1, y1, x2, y2, gdp, start_cash, high_1, low_1
        

        def section_dictate_to_web_app(proof, gdp, one):
            st.caption(f"{'__'*25}\n{'__'*25}")
            st.header(f"> __[{namer} vs SPY]__")
            st.write(f" - Start Position [{self.today_stamp}] ")
            st.write(f" - Today's Position [{str(datetime.now())[:10]}] ")
            st.write(f"Total Allocation == {total_allocation}%")
            st.table(gdp)
            st.write(f" - __Proof returns__")
            st.write(f" - {namer}")
            st.write(f" - Winning Stock Picks [Positive Return] = {len(proof_2['ticker'])}/{divisor}, [{winning_percentage}%] ")
            st.write(f" - Stocks Outperforming The SPY  = {len(proof_3['ticker'])}/{divisor}, [{beat_spy_percentage}%   ]")
            st.write(f" - __Initial Portfolio Optimization Modeled On {self.today_stamp}__")
            proof = proof.sort_values("return", ascending=False)
            proof["rank"] = proof["return"].rank(ascending=False)
            st.table(proof.set_index(["rank", "companyName", "ticker"]))
            
            weiner = pd.DataFrame(one[one['since_open'] >= 10.0])
            davis = pd.DataFrame(one[one['since_open'] <= -10.0])
            return weiner, davis            


        def section_save_and_record(gdp, proof, proof_spy, one):
            if self.graphit:
                fig, ax = plt.subplots()
                ax.plot(one["portfolio"], color='black', lw=1, marker='.', ms=10, label='Portfolio')
                ax.plot(weiner['portfolio'], color='blue', lw=1, marker='.', ms=10, label='Up10')
                ax.plot(davis['portfolio'], color='red', lw=1, marker='.', ms=10, label='Down10')
                ax.axhline(start_cash, color='black', lw=1)
                ax.axhline(start_cash * 1.1, color='green', lw=1)
                ax.axhline(start_cash * 0.9, color='red', lw=1)
                try:
                    ax.plot(x1, y1, color="green", marker="*", ms=20, label="High Watermark")
                    ax.plot(x2, y2, color="red", marker="X", ms=17, label="low Watermark")
                except:
                    print("")
                plt.legend(loc='best')
                st.subheader("__Portfolio Balance History__")
                st.pyplot(fig)
                
                # two=pd.DataFrame(one.copy()).reset_index(inplace=True)
                # weiner.reset_index(inplace=True)
                # davis.reset_index(inplace=True)            
                            
                # fig = go.Figure()
                # fig.add_trace(go.Scatter(x=two['date'], y=one['portfolio'], name='Portfolio',
                #                         mode='lines+markers', line=dict(color='black', width=2)))
                # fig.add_trace(go.Scatter(x=weiner['date'], y=weiner['portfolio'], name='Winners',
                #                         mode='lines+markers', line=dict(color='royalblue', width=2)))
                # fig.add_trace(go.Scatter(x=davis['date'], y=davis['portfolio'], name='Losers',
                #                         mode='lines+markers', line=dict(color='firebrick', width=2)))
                # fig.add_hline(y=2750.0, line_dash="dot", line=dict(color='forestgreen', width=2))
                # fig.add_hline(y=2250.0, line_dash="dot", line=dict(color='darkred', width=2))
                # fig.update_layout(
                #     margin=dict(l=20, r=20, t=20, b=20),
                #     paper_bgcolor="LightSteelBlue",
                # )
                # st.plotly_chart(fig)
                
            st.write(f" * __HIGH WATERMARK:__ ${high_1} __[{round(((high_1 - start_cash) / start_cash) * 100, 2)}%]__")
            st.write(f" * __LOW WATERMARK:__ ${low_1} __[{round(((low_1 - start_cash) / start_cash) * 100, 2)}%]__")
            st.caption(f"{'__'*25}\n{'__'*25}")
            

            if self.save_output == True:
                gdp = pd.DataFrame(gdp)
                proof = pd.DataFrame(proof)
                proof_spy = pd.DataFrame(proof_spy)
                one = pd.DataFrame(one)
                del one['since_open']
                                
                gdp.to_csv(self.final_loc / f"spy_vs_{namer}.csv")                
                proof.to_csv(self.final_loc / f"{namer}.csv")                                
                proof_spy.to_csv(self.final_loc / f"spy.csv")
                one.to_csv(self.final_loc / f"one_{self.namer}.csv")
                
                def convert_df(df):
                    return df.to_csv().encode('utf-8')

                csv = convert_df(proof)
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name=f"{str(self.final_loc)}/{str(namer)}.csv",
                    mime='text/csv',
                    key=str(namer),
                )
                return 


        def weiner_or_whore(one):
            path101 = Path(f"reports/measurements/")
            fd = pd.DataFrame(pd.read_csv(path101 / "dick_measurement.csv")).set_index('date')

            def mini():            
                for i in one['since_open']:
                    if i >= 10.0:
                        hood_rat_status = 'Gator'
                        return hood_rat_status
                    elif i <= -10.0:
                        hood_rat_status = 'Whore'
                        return hood_rat_status
                    else:
                        hood_rat_status = 'curious'
                        return hood_rat_status
            
            hood_rat_status = mini()
            if hood_rat_status == "Gator":
                fd[f"{self.namer}"][f"{self.og_day}"] = +10.0
            elif hood_rat_status == 'Whore':
                fd[f"{self.namer}"][f"{self.og_day}"] = -10.0
            else:
                fd[f"{self.namer}"][f"{self.og_day}"] = 'curious'
            fd.to_csv(path101 / "dick_measurement.csv")


        proof, df_close = section_proof_df()            
        proof_spy, winning_percentage, beat_spy_percentage, proof_2, proof_3 = section_spy_df()            
        one, x1, y1, x2, y2, gdp, start_cash, high_1, low_1 = section_one_df(df_close)            
        weiner, davis = section_dictate_to_web_app(proof, gdp, one)                
        section_save_and_record(gdp, proof, proof_spy, one)
        weiner_or_whore(one)            


    def setup(self, portfolio_option):
        if 'maximum_sharpe_ratio' in portfolio_option:
            maximum_sharpe_ratio = pd.read_csv(self.final_loc / "maximum_sharpe_ratio.csv")#.set_index("rank")
            maximum_sharpe_ratio = maximum_sharpe_ratio.rename(columns={'symbol': 'ticker'})
            self.performance(maximum_sharpe_ratio[["ticker", "allocation"]], "maximum_sharpe_ratio")
            time.sleep(1.3)

        if 'minimum_volatility_portfolio' in portfolio_option:
            minimum_volatility_portfolio = pd.read_csv(self.final_loc / "minimum_volatility_portfolio.csv")#.set_index("rank")
            minimum_volatility_portfolio = minimum_volatility_portfolio.rename(columns={'symbol': 'ticker'})
            self.performance(minimum_volatility_portfolio[["ticker", "allocation"]],"minimum_volatility_portfolio",)
            time.sleep(1.3)

        if 'maximum_sharpe_equalWT' in portfolio_option:
            maximum_sharpe_equalWT = pd.read_csv(self.final_loc / "maximum_sharpe_equalWT.csv")#.set_index("rank")
            maximum_sharpe_equalWT = maximum_sharpe_equalWT.rename(columns={'symbol': 'ticker'})
            self.performance(maximum_sharpe_equalWT[["ticker", "allocation"]], "maximum_sharpe_equalWT")
            time.sleep(1.3)        

        if 'monte_carlo_cholesky' in portfolio_option:
            monte_carlo_cholesky = pd.read_csv(self.final_loc / "monte_carlo_cholesky.csv")#.set_index("rank")zz
            monte_carlo_cholesky = monte_carlo_cholesky.rename(columns={'symbol': 'ticker'})
            self.performance(monte_carlo_cholesky[["ticker", "allocation"]], "monte_carlo_cholesky")
            time.sleep(1.3)

        print('\n', f">>> {self.og_day} <<<", '\n')
        return







class Proof_of_Concept(object):
    def __init__(self, today_stamp, ender_date=str(datetime.now())[:10], save_output=True, graphit=True):
        self.save_output = save_output
        self.graphit = graphit
        self.today_stamp = str(today_stamp)[:10]
        self.saveMonth = self.today_stamp[:7]
        self.final_loc = Path(f"reports/port_results/{self.saveMonth}/{self.today_stamp}/")
        self.saveReport = Path(f"reports/portfolio/{self.saveMonth}/{self.today_stamp}/")
        self.saveAdvisor = Path(f"data/advisor/{self.saveMonth}/{self.today_stamp}/")
        self.saveProof = Path(f"data/proof/{self.today_stamp}/{ender_date}/")
        if not self.final_loc.exists():
            self.final_loc.mkdir(parents=True)        
        if not self.saveReport.exists():
            self.saveReport.mkdir(parents=True)        
        if not self.saveAdvisor.exists():
            self.saveAdvisor.mkdir(parents=True)
        if not self.saveProof.exists():
            self.saveProof.mkdir(parents=True)
        self.day = int(str(today_stamp)[8:10])
        self.month = int(str(today_stamp)[5:7])
        self.year = int(str(today_stamp)[:4])
        self.starter_date = datetime(self.year, self.month, self.day) + timedelta(days=1)
        self.og_day = str(self.today_stamp)[:10]


    def setup(self, portfolio_file, namer, data, initial_cash=2500):
        og_wt = portfolio_file['allocation'].sum()
        new_wt_lst = []
        for i in portfolio_file['allocation']:
            new_wt_lst.append((i * 100) / og_wt)
        portfolio_file['allocation'] = (new_wt_lst)        
        portfolio_file = pd.DataFrame(portfolio_file).sort_values('ticker')
                
        self.namer = namer
        self.initial_cash = initial_cash
        divisor = len(portfolio_file["ticker"])
        total_allocation = portfolio_file["allocation"].sum() / 100
        
        df = pd.DataFrame(data.loc[self.starter_date:]).round(2)
        df = df.reindex(sorted(df.columns), axis=1)

        proof = pd.DataFrame(portfolio_file[["ticker", "allocation"]]).sort_values("ticker", ascending=True)
        
        b = []
        for i in proof["ticker"]:
            b.append(company_longName(i))
        proof["companyName"] = b

        proof['start_price'] = list(df.iloc[0])
        proof['current_price'] = list(df.iloc[-1])   

        proof["initial_investment"] = round(self.initial_cash * (proof["allocation"] / 100), 2)
        proof["shares"] = round(proof["initial_investment"] / proof["start_price"], 2)
        proof["cash_now"] = round(proof["shares"] * proof["current_price"], 2)
        proof["return"] = round(((proof["cash_now"] - proof["initial_investment"]) / proof["initial_investment"]) * 100,2,)


        port_tics=['SPY']
        df_close = pd.DataFrame()
        df_open = pd.DataFrame()
        hammerTime = Ticker(
            port_tics,
            asynchronous=True,
            formatted=False,
            backoff_factor=0.34,
            validate=True,
            verify=True,
        )
        hammer_hist = hammerTime.history(start=self.today_stamp).reset_index().set_index('date')
        hammer_hist.index = pd.to_datetime(hammer_hist.index)
        hammer_hist = hammer_hist.rename(columns={'symbol': 'ticker'})
        hammer_hist = hammer_hist.drop_duplicates(subset=['ticker'])
        spy_hist = pd.DataFrame(hammer_hist.copy())

        proof_spy = pd.DataFrame(["SPY"], columns=["SPY"])
        proof_spy["start_price"] = round(spy_hist["open"][0], 2)
        proof_spy["current_price"] = round(spy_hist["adjclose"][0], 2)
        proof_spy["initial_investment"] = round(self.initial_cash / len(proof_spy["SPY"]), 2)
        proof_spy["shares"] = round(proof_spy["initial_investment"] / proof_spy["start_price"], 2)
        proof_spy["cash_now"] = round(proof_spy["shares"] * proof_spy["current_price"], 2)
        proof_spy["return"] = round(((proof_spy["cash_now"] - proof_spy["initial_investment"])/ proof_spy["initial_investment"])* 100,2,)
        

        high_watermark_spy = round(proof_spy["return"].max(), 2)
        low_watermark_spy = round(proof_spy["return"].min(), 2)
        beat_num = proof_spy["return"][0]
        proof_2 = proof[proof["return"] > 0.0]
        proof_3 = proof_2[proof_2["return"] > beat_num]
        winning_percentage = round((len(proof_2["ticker"]) / divisor) * 100, 2)
        beat_spy_percentage = round((len(proof_3["ticker"]) / divisor), 2)

        one = pd.DataFrame(df.copy())
        shares = []
        allocation_lst = list(proof["allocation"])
        for k, v in enumerate(list(proof["ticker"])):
            shares.append(((allocation_lst[k] / 100) * initial_cash) / one[v].iloc[0])
        for k, v in enumerate(list(proof["ticker"])):
            one[v] = one[v] * shares[k]
        lst = list(proof["ticker"])
        one["portfolio"] = one[lst].sum(axis=1)
        eno = one.reset_index()
        start_cash = round(proof["initial_investment"].sum(), 2)
        avg_1 = round(one["portfolio"].mean(), 2)
        high_1 = round(one["portfolio"].max(), 2)
        low_1 = round(one["portfolio"].min(), 2)
        mean_watermark = round(((avg_1 - start_cash) / start_cash) * 100, 2)
        high_watermark = round(((high_1 - start_cash) / start_cash) * 100, 2)
        low_watermark = round(((low_1 - start_cash) / start_cash) * 100, 2)
        mean_watermark_spy = round(proof_spy["return"].mean(), 2)
        high_watermark_spy = round(proof_spy["return"].max(), 2)
        low_watermark_spy = round(proof_spy["return"].min(), 2)
        beat_num = proof_spy["return"][0]
        proof_2 = proof[proof["return"] > 0.0]
        proof_3 = proof_2[proof_2["return"] > beat_num]                  
        x1 = eno[eno["portfolio"] == eno["portfolio"].max()]["date"]
        y1 = one["portfolio"].max()
        x2 = eno[eno["portfolio"] == eno["portfolio"].min()]["date"]
        y2 = one["portfolio"].min()
        for i in list(one["portfolio"]):
            if float(i) > high_1:
                high_1 = float(i)
            else:
                pass  
        one["since_open"] = round(((one["portfolio"] - start_cash) / start_cash) * 100, 2)
        try:
            act_ror = round(((list(one["portfolio"])[-1] - list(one["portfolio"])[0])/ list(one["portfolio"])[0])* 100,2,)
        except Exception:
            act_ror = 'ongoing'


        gdp = pd.DataFrame(["Recommended Stocks", "SPY Index"], columns=["strategy_vs_benchmark"])
        gdp["starting_money"] = [
            f"${round(list(one['portfolio'])[0],2)}",
            f"${round(proof_spy['initial_investment'].sum(),2)}",
        ]
        gdp["ending_money"] = [
            f"${round(list(one['portfolio'])[-1],2)}",
            f"${round(proof_spy['cash_now'].sum(), 2)}",
        ]
        gdp["return"] = [
            f"{round(act_ror,2)}%",
            f"{round(float(proof_spy['return']),2)}%",
        ]
        gdp["mean_mark"] = [
            f"{mean_watermark}%",
            f"{mean_watermark_spy}%",
        ]        
        gdp["high_mark"] = [
            f"{high_watermark}%",
            f"{high_watermark_spy}%",
        ]
        gdp["low_mark"] = [
            f"{low_watermark}%",
            f"{low_watermark_spy}%",
        ]                        
        gdp = gdp.set_index("strategy_vs_benchmark")


        st.caption(f"{'__'*25}\n{'__'*25}")
        st.header(f"> __[{self.namer} vs SPY]__")
        st.write(f" - Start Position [{self.starter_date}] ")
        st.write(f" - Today's Position [{str(datetime.now())[:10]}] ")
        st.write(f" - Total Allocation: {round(total_allocation*100,2)}%")
        st.table(gdp)
        st.write(f" - __Proof returns__")
        st.write(f" - {self.namer}")
        st.write(f" - Winning Stock Picks [Positive Return] = {len(proof_2['ticker'])}/{divisor}, [{winning_percentage}%] ")
        st.write(f" - Stocks Outperforming The SPY  = {len(proof_3['ticker'])}/{divisor}, [{beat_spy_percentage}%   ]")
        st.write(f" - __Initial Portfolio Optimization Modeled On {self.starter_date}__")

        proof = proof.sort_values("return", ascending=False)
        proof["rank"] = proof["return"].rank(ascending=False)
        st.table(proof.set_index(["rank", "companyName", "ticker"]))

        one["since_open"] = round(((one["portfolio"] - start_cash) / start_cash) * 100, 2)
        
        two = pd.DataFrame(one.copy())
        weiner = pd.DataFrame(two[two['since_open'] >= 10.0])
        davis = pd.DataFrame(two[two['since_open'] <= -10.0])


        if self.graphit:
            fig, ax = plt.subplots()
            ax.plot(two["portfolio"], color='black', lw=1, marker='.', ms=10, label='Portfolio')
            ax.plot(weiner['portfolio'], color='blue', lw=1, marker='.', ms=10, label='Up10')
            ax.plot(davis['portfolio'], color='red', lw=1, marker='.', ms=10, label='Down10')
            ax.axhline(start_cash, color='black', lw=1)
            ax.axhline(start_cash * 1.1, color='green', lw=1)
            ax.axhline(start_cash * 0.9, color='red', lw=1)
            try:
                ax.plot(x1, y1, color="green", marker="*", ms=20, label="High Watermark")
                ax.plot(x2, y2, color="red", marker="X", ms=17, label="low Watermark")
            except:
                print("")
            plt.legend(loc='best')
            st.subheader("__Portfolio Balance History__")
            st.pyplot(fig)
            
            two.reset_index(inplace=True)
            weiner.reset_index(inplace=True)
            davis.reset_index(inplace=True)            
                        
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=two['date'], y=one['portfolio'], name='Portfolio',
                                    mode='lines+markers', line=dict(color='black', width=2)))
            fig.add_trace(go.Scatter(x=weiner['date'], y=weiner['portfolio'], name='Winners',
                                    mode='lines+markers', line=dict(color='royalblue', width=2)))
            fig.add_trace(go.Scatter(x=davis['date'], y=davis['portfolio'], name='Losers',
                                    mode='lines+markers', line=dict(color='firebrick', width=2)))
            fig.add_hline(y=2750.0, line_dash="dot", line=dict(color='forestgreen', width=2))
            fig.add_hline(y=2250.0, line_dash="dot", line=dict(color='darkred', width=2))
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="LightSteelBlue",
            )
            st.plotly_chart(fig)
                        

            
        st.write(f" * __HIGH WATERMARK:__ ${high_1} __[{round(((high_1 - start_cash) / start_cash) * 100, 2)}%]__")
        st.write(f" * __LOW WATERMARK:__ ${low_1} __[{round(((low_1 - start_cash) / start_cash) * 100, 2)}%]__")

        def weiner_or_whore(one):
            for i in one['since_open']:
                if i >= 10.0:
                    hood_rat_status = 'Gator'
                    return hood_rat_status
                elif i <= -10.0:
                    hood_rat_status = 'Whore'
                    return hood_rat_status
                else:
                    hood_rat_status = 'curious'
                    return hood_rat_status
        hood_rat_status = weiner_or_whore(one)

        path101 = Path(f"reports/measurements/")
        fd = pd.DataFrame(pd.read_csv(path101 / "dick_measurement.csv")).set_index('date')
        if hood_rat_status == "Gator":
            fd[f"{self.namer}"][f"{self.og_day}"] = +10.0
        elif hood_rat_status == 'Whore':
            fd[f"{self.namer}"][f"{self.og_day}"] = -10.0
        else:
            fd[f"{self.namer}"][f"{self.og_day}"] = 'curious'
        fd.to_csv(path101 / "dick_measurement.csv")      


        if self.save_output == True:
            gdp = pd.DataFrame(gdp)
            proof = pd.DataFrame(proof)
            proof_spy = pd.DataFrame(proof_spy)
            one = pd.DataFrame(one)
            del one['since_open']
                            
            gdp.to_csv(self.final_loc / f"spy_vs_{namer}.csv")                
            proof.to_csv(self.final_loc / f"{namer}.csv")                                
            proof_spy.to_csv(self.final_loc / f"spy.csv")
            one.to_csv(self.final_loc / f"one_{self.namer}.csv")

            def convert_df(df):
                return df.to_csv().encode('utf-8')
            
            csv = convert_df(proof)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f"{str(self.final_loc)}/{str(self.namer)}.csv",
                mime='text/csv',
                key=str(self.namer),
            )
            return 
        else:
            return 






class Proof_of_Concept_Builder(object):
    
    def __init__(self, today_stamp, ender_date=str(datetime.now())[:10], save_output=True, graphit=True):
        self.save_output = save_output
        self.graphit = graphit
        self.today_stamp = str(today_stamp)[:10]
        self.saveMonth = self.today_stamp[:7]
        self.final_loc = Path(f"reports/port_results/{self.saveMonth}/{self.today_stamp}/")
        self.saveReport = Path(f"reports/portfolio/{self.saveMonth}/{self.today_stamp}/")
        self.saveAdvisor = Path(f"data/advisor/{self.saveMonth}/{self.today_stamp}/")
        self.saveProof = Path(f"data/proof/{self.today_stamp}/{ender_date}/")
        if not self.final_loc.exists():
            self.final_loc.mkdir(parents=True)        
        if not self.saveReport.exists():
            self.saveReport.mkdir(parents=True)        
        if not self.saveAdvisor.exists():
            self.saveAdvisor.mkdir(parents=True)
        if not self.saveProof.exists():
            self.saveProof.mkdir(parents=True)
        self.day = int(str(today_stamp)[8:10])
        self.month = int(str(today_stamp)[5:7])
        self.year = int(str(today_stamp)[:4])
        self.starter_date = datetime(self.year, self.month, self.day) + timedelta(days=1)
        self.og_day = str(self.today_stamp)[:10]


    def setup(self, portfolio_file, namer, data, initial_cash=2500):
        og_wt = portfolio_file['allocation'].sum()
        new_wt_lst = []
        for i in portfolio_file['allocation']:
            new_wt_lst.append((i * 100) / og_wt)
        portfolio_file['allocation'] = (new_wt_lst)        
        portfolio_file = pd.DataFrame(portfolio_file).sort_values('ticker')
        
        self.namer = namer
        self.initial_cash = initial_cash
        divisor = len(portfolio_file["ticker"])
        total_allocation = portfolio_file["allocation"].sum() / 100
        port_tics = sorted(list(portfolio_file["ticker"]))
        df = pd.DataFrame(data.loc[self.today_stamp:]).round(2)

        proof = pd.DataFrame(portfolio_file[["ticker", "allocation"]])
        proof = proof.sort_values("ticker")
        b = []
        for i in proof["ticker"]:
            b.append(company_longName(i))
        proof["companyName"] = b


        df_close = pd.DataFrame()
        df_open = pd.DataFrame()
        hammerTime = Ticker(
            port_tics,
            asynchronous=True,
            formatted=False,
            backoff_factor=0.34,
            validate=True,
            verify=True,
        )
        hammer_hist = hammerTime.history(start=self.today_stamp).reset_index().set_index('date')
        hammer_hist.index = pd.to_datetime(hammer_hist.index)
        hammer_hist = hammer_hist.rename(columns={'symbol': 'ticker'})
        hammer_hist = hammer_hist.drop_duplicates(subset=['ticker'])
        for i in port_tics:
            try:
                z = pd.DataFrame(hammer_hist[hammer_hist['ticker'] == i]['adjclose'])
                df_close[i] = z
            except:
                print(f"failed ticker {i}")
                proof = proof.drop(proof[proof.ticker == i].index)
                port_tics.remove(i)
        for i in port_tics:
            try:
                z = pd.DataFrame(hammer_hist[hammer_hist['ticker'] == i]['open'])
                df_open[i] = z
            except:
                print(f"failed ticker {i}")
                proof = proof.drop(proof[proof.ticker == i].index)
                port_tics.remove(i)

        try:
            proof['start_price'] = list(df_open.iloc[0])
        except Exception:
            proof['start_price'] = list(df_close.iloc[0])
        proof["current_price"] = list(df_close.iloc[-1])
        proof["initial_investment"] = round(self.initial_cash * (proof["allocation"] / 100), 2)
        proof["shares"] = round(proof["initial_investment"] / proof["start_price"], 2)
        proof["cash_now"] = round(proof["shares"] * proof["current_price"], 2)
        proof["return"] = round(((proof["cash_now"] - proof["initial_investment"])/ proof["initial_investment"])* 100,2,)

        port_tics=['SPY']
        df_close = pd.DataFrame()
        df_open = pd.DataFrame()
        hammerTime = Ticker(
            port_tics,
            asynchronous=True,
            formatted=False,
            backoff_factor=0.34,
            validate=True,
            verify=True,
        )
        hammer_hist = hammerTime.history(start=self.today_stamp).reset_index().set_index('date')
        hammer_hist.index = pd.to_datetime(hammer_hist.index)
        hammer_hist = hammer_hist.rename(columns={'symbol': 'ticker'})
        hammer_hist = hammer_hist.drop_duplicates(subset=['ticker'])
        spy_hist = pd.DataFrame(hammer_hist.copy())

        proof_spy = pd.DataFrame(["SPY"], columns=["SPY"])
        proof_spy["start_price"] = spy_hist["open"][0]
        proof_spy["current_price"] = spy_hist["adjclose"][0]
        proof_spy["initial_investment"] = round(self.initial_cash / len(proof_spy["SPY"]), 2)
        proof_spy["shares"] = round(proof_spy["initial_investment"] / proof_spy["start_price"], 2)
        proof_spy["cash_now"] = round(proof_spy["shares"] * proof_spy["current_price"], 2)
        proof_spy["return"] = round(((proof_spy["cash_now"] - proof_spy["initial_investment"])/ proof_spy["initial_investment"])* 100,2,)
        

        high_watermark_spy = round(proof_spy["return"].max(), 2)
        low_watermark_spy = round(proof_spy["return"].min(), 2)
        beat_num = proof_spy["return"][0]
        proof_2 = proof[proof["return"] > 0.0]
        proof_3 = proof_2[proof_2["return"] > beat_num]
        winning_percentage = round((len(proof_2["ticker"]) / divisor) * 100, 2)
        beat_spy_percentage = round((len(proof_3["ticker"]) / divisor), 2)


        one = pd.DataFrame(df.copy())
        shares = []
        allocation_lst = list(proof["allocation"])
        for k, v in enumerate(list(proof["ticker"])):
            shares.append(((allocation_lst[k] / 100) * initial_cash) / one[v].iloc[0])
        for k, v in enumerate(list(proof["ticker"])):
            one[v] = one[v] * shares[k]
        lst = list(proof["ticker"])
        one["portfolio"] = one[lst].sum(axis=1)
        eno = one.reset_index()
        start_cash = round(proof["initial_investment"].sum(), 2)
        avg_1 = round(one["portfolio"].mean(), 2)
        high_1 = round(one["portfolio"].max(), 2)
        low_1 = round(one["portfolio"].min(), 2)
        mean_watermark = round(((avg_1 - start_cash) / start_cash) * 100, 2)
        high_watermark = round(((high_1 - start_cash) / start_cash) * 100, 2)
        low_watermark = round(((low_1 - start_cash) / start_cash) * 100, 2)
        mean_watermark_spy = round(proof_spy["return"].mean(), 2)
        high_watermark_spy = round(proof_spy["return"].max(), 2)
        low_watermark_spy = round(proof_spy["return"].min(), 2)
        beat_num = proof_spy["return"][0]
        proof_2 = proof[proof["return"] > 0.0]
        proof_3 = proof_2[proof_2["return"] > beat_num]                  
        x1 = eno[eno["portfolio"] == eno["portfolio"].max()]["date"]
        y1 = one["portfolio"].max()
        x2 = eno[eno["portfolio"] == eno["portfolio"].min()]["date"]
        y2 = one["portfolio"].min()
        for i in list(one["portfolio"]):
            if float(i) > high_1:
                high_1 = float(i)
            else:
                pass  
        one["since_open"] = round(((one["portfolio"] - start_cash) / start_cash) * 100, 2)
        try:
            act_ror = round(((list(one["portfolio"])[-1] - list(one["portfolio"])[0])/ list(one["portfolio"])[0])* 100,2,)
        except Exception:
            act_ror = 'ongoing'


        gdp = pd.DataFrame(["Recommended Stocks", "SPY Index"], columns=["strategy_vs_benchmark"])
        gdp["starting_money"] = [
            f"${round(list(one['portfolio'])[0],2)}",
            f"${round(proof_spy['initial_investment'].sum(),2)}",
        ]
        gdp["ending_money"] = [
            f"${round(list(one['portfolio'])[-1],2)}",
            f"${round(proof_spy['cash_now'].sum(), 2)}",
        ]
        gdp["return"] = [
            f"{round(act_ror,2)}%",
            f"{round(float(proof_spy['return']),2)}%",
        ]
        gdp["mean_mark"] = [
            f"{mean_watermark}%",
            f"{mean_watermark_spy}%",
        ]        
        gdp["high_mark"] = [
            f"{high_watermark}%",
            f"{high_watermark_spy}%",
        ]
        gdp["low_mark"] = [
            f"{low_watermark}%",
            f"{low_watermark_spy}%",
        ]                        
        gdp = gdp.set_index("strategy_vs_benchmark")


        st.caption(f"{'__'*25}\n{'__'*25}")
        st.header(f"> __[{self.namer} vs SPY]__")
        st.write(f" - Start Position [{self.starter_date}] ")
        st.write(f" - Today's Position [{str(datetime.now())[:10]}] ")
        st.write(f" - Total Allocation: {round(total_allocation*100,2)}%")
        st.table(gdp)
        st.write(f" - __Proof returns__")
        st.write(f" - {self.namer}")
        st.write(f" - Winning Stock Picks [Positive Return] = {len(proof_2['ticker'])}/{divisor}, [{winning_percentage}%] ")
        st.write(f" - Stocks Outperforming The SPY  = {len(proof_3['ticker'])}/{divisor}, [{beat_spy_percentage}%   ]")
        st.write(f" - __Initial Portfolio Optimization Modeled On {self.starter_date}__")

        proof = proof.sort_values("return", ascending=False)
        proof["rank"] = proof["return"].rank(ascending=False)
        st.table(proof.set_index(["rank", "companyName", "ticker"]))

        one["since_open"] = round(((one["portfolio"] - start_cash) / start_cash) * 100, 2)
        weiner = pd.DataFrame(one[one['since_open'] >= 10.0])
        davis = pd.DataFrame(one[one['since_open'] <= -10.0])


        if self.graphit:
            fig, ax = plt.subplots()
            ax.plot(one["portfolio"], color='black', lw=1, marker='.', ms=10, label='Portfolio')
            ax.plot(weiner['portfolio'], color='blue', lw=1, marker='.', ms=10, label='Up10')
            ax.plot(davis['portfolio'], color='red', lw=1, marker='.', ms=10, label='Down10')
            ax.axhline(start_cash, color='black', lw=1)
            ax.axhline(start_cash * 1.1, color='green', lw=1)
            ax.axhline(start_cash * 0.9, color='red', lw=1)
            try:
                ax.plot(x1, y1, color="green", marker="*", ms=20, label="High Watermark")
                ax.plot(x2, y2, color="red", marker="X", ms=17, label="low Watermark")
            except:
                print("")
            plt.legend(loc='best')
            st.subheader("__Portfolio Balance History__")
            st.pyplot(fig)
            
            # two=pd.DataFrame(one.copy()).reset_index(inplace=True)
            # weiner.reset_index(inplace=True)
            # davis.reset_index(inplace=True)            
                        
            # fig = go.Figure()
            # fig.add_trace(go.Scatter(x=two['date'], y=one['portfolio'], name='Portfolio',
            #                         mode='lines+markers', line=dict(color='black', width=2)))
            # fig.add_trace(go.Scatter(x=weiner['date'], y=weiner['portfolio'], name='Winners',
            #                         mode='lines+markers', line=dict(color='royalblue', width=2)))
            # fig.add_trace(go.Scatter(x=davis['date'], y=davis['portfolio'], name='Losers',
            #                         mode='lines+markers', line=dict(color='firebrick', width=2)))
            # fig.add_hline(y=2750.0, line_dash="dot", line=dict(color='forestgreen', width=2))
            # fig.add_hline(y=2250.0, line_dash="dot", line=dict(color='darkred', width=2))
            # fig.update_layout(
            #     margin=dict(l=20, r=20, t=20, b=20),
            #     paper_bgcolor="LightSteelBlue",
            # )
            # st.plotly_chart(fig)
            
        st.write(f" * __HIGH WATERMARK:__ ${high_1} __[{round(((high_1 - start_cash) / start_cash) * 100, 2)}%]__")
        st.write(f" * __LOW WATERMARK:__ ${low_1} __[{round(((low_1 - start_cash) / start_cash) * 100, 2)}%]__")
        

        def weiner_or_whore(one):
            for i in one['since_open']:
                if i >= 10.0:
                    hood_rat_status = 'Gator'
                    return hood_rat_status
                elif i <= -10.0:
                    hood_rat_status = 'Whore'
                    return hood_rat_status
                else:
                    hood_rat_status = 'curious'
                    return hood_rat_status
        hood_rat_status = weiner_or_whore(one)

        path101 = Path(f"reports/measurements/")
        fd = pd.DataFrame(pd.read_csv(path101 / "dick_measurement.csv")).set_index('date')
        if hood_rat_status == "Gator":
            fd[f"{self.namer}"][f"{self.og_day}"] = +10.0
        elif hood_rat_status == 'Whore':
            fd[f"{self.namer}"][f"{self.og_day}"] = -10.0
        else:
            fd[f"{self.namer}"][f"{self.og_day}"] = 'curious'
        fd.to_csv(path101 / "dick_measurement.csv")      


        if self.save_output == True:
            gdp = pd.DataFrame(gdp)
            proof = pd.DataFrame(proof)
            proof_spy = pd.DataFrame(proof_spy)
            one = pd.DataFrame(one)
            del one['since_open']
                            
            gdp.to_csv(self.final_loc / f"spy_vs_{namer}.csv")                
            proof.to_csv(self.final_loc / f"{namer}.csv")                                
            proof_spy.to_csv(self.final_loc / f"spy.csv")
            one.to_csv(self.final_loc / f"one_{self.namer}.csv")

            def convert_df(df):
                return df.to_csv().encode('utf-8')
            
            csv = convert_df(proof)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f"{str(self.final_loc)}/{str(self.namer)}.csv",
                mime='text/csv',
                key=str(self.namer),
            )
            return 
        else:
            return 
