from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd
from src import yfinance_data as yf_data


# Import the backtrader platform
import backtrader as bt

if __name__ == '__main__':
    dataframe = yf_data.get_data("399997.SZ", datetime.datetime.now() - datetime.timedelta(days=1),
                                 datetime.datetime.now(), "1m")
    # dataframe 增加一列，Date 与 index 一致
    dataframe['Date'] = dataframe.index
    print(dataframe)
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.addstrategy(bt.Strategy)
    data = bt.feeds.PandasData(dataname=dataframe,
                               datetime='Date',
                               nocase=True,
                               )
    cerebro.adddata(data)

    # Run over everything
    cerebro.run()
    # Plot the result
    cerebro.plot(style='bar')