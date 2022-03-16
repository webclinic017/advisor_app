import warnings

warnings.filterwarnings("ignore")
from datetime import datetime
import backtrader as bt
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [15, 7]
plt.rcParams["figure.dpi"] = 134

from pathlib import Path
from datetime import datetime

# today = str(datetime.now())[:10]
# savePlot = Path(f"report/portfolio_{today}/IIIII_evaluate")
# if not savePlot.exists():
#     savePlot.mkdir(parents=True)


class SmaCross(bt.SignalStrategy, object):
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=2), bt.ind.SMA(period=20)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)
        self.signal_add(bt.SIGNAL_LONGEXIT, crossover)
        self.signal_add(bt.SIGNAL_SHORT, crossover)


def run_bt_SMA(
    ticker, start_date=datetime(2011, 1, 1), end_date=datetime(2012, 12, 31)
):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)
    start_cash = 10000.00

    cerebro.broker.setcash(start_cash)
    data0 = bt.feeds.YahooFinanceData(
        dataname=ticker, fromdate=start_date, todate=end_date
    )
    cerebro.adddata(data0)

    cerebro.run()
    cerebro.plot(tic_name=f"{ticker}_bt_SMA_.png")

    print("\nStarting Portfolio Value: %.2f" % start_cash)
    print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue(), "\n")

    print("\nStarting Portfolio Value: %.2f" % start_cash)
    print("Final Cash Value: %.2f" % cerebro.broker.get_cash(), "\n")
    print("Final position Value: %.2f" % cerebro.broker.get_fundvalue(), "\n")
    print("Final position Value: %.2f" % cerebro.broker.get_fundshares(), "\n")
    print(
        "Final Portfolio Value: %.2f"
        % (
            float(
                cerebro.broker.get_fundvalue() * float(cerebro.broker.get_fundshares())
            )
            + float(cerebro.broker.get_cash())
        ),
        "\n",
    )
    return


if __name__ == "__main__":
    for i in ["^GSPC", "^DJI"]:
        run_bt_SMA(ticker=i)
