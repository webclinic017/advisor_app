from datetime import datetime
import backtrader as bt

# from chapter_2_utils import MyBuySell


class MyBuySell(bt.observers.BuySell):
    plotlines = dict(
        buy=dict(marker="^", markersize=8.0, color="blue", fillstyle="full"),
        sell=dict(marker="v", markersize=8.0, color="red", fillstyle="full"),
    )


# create the strategy using a signal
class SmaSignal(bt.Signal):
    params = (("period", 20),)

    def __init__(self):
        self.lines.signal = self.data - bt.ind.SMA(period=self.p.period)


# download data
data = bt.feeds.YahooFinanceData(
    dataname="/home/gordon/modern_millennial_market_mapping/src/models/backtest/z_test_env/AAPL.pkl",
    fromdate=datetime(2021, 1, 1),
    todate=datetime.now(),
)

# create a Cerebro entity
cerebro = bt.Cerebro(stdstats=False)

# set up the backtest
cerebro.adddata(data)
cerebro.broker.setcash(1000.0)
cerebro.add_signal(bt.SIGNAL_LONG, SmaSignal)
cerebro.addobserver(MyBuySell)
cerebro.addobserver(bt.observers.Value)

# run backtest
print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
x = cerebro.run()
print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")

# plot results
cerebro.plot(iplot=True, volume=False)
