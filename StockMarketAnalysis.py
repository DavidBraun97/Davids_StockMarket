import pandas as pd
import datetime
import matplotlib.pyplot as plt
import time

from utility.utils import *

plt.style.use('ggplot')


##  Gather data ##
tickers = ["AAPL","GOOG",'MSFT']
#print("##  Pulling live stock data.  ##")
start = datetime.datetime(2016,1,1)
#pullstockfrom_av_long(tickers,start)

# for ticker in tickers:
#     stock_df = getdffromcsv(ticker)
#     visualize_stocks_individually(stock_df, ticker)
#     adjClose_df = pd.DataFrame(stock_df['adj. Close'])
#     stock_return = adjClose_df.apply(lambda x: x / x[-1])
#     stock_return.head() - 1
#     stock_return.plot(grid = True).axhline(y = 1, color = "black", lw = 2)
#     plt.show()


aapl_df = getdffromcsv("AAPL")
goog_df = getdffromcsv("GOOG")
msft_df = getdffromcsv("MSFT")
stocks_df = pd.DataFrame({'APPL Adj. Close': aapl_df['adj. Close'], 'GOOG Adj. Close': goog_df['adj. Close'], 'MSFT Adj. Close': msft_df['adj. Close']})

## Stock revenue
stock_return = stocks_df.apply(lambda x: x / x[-1])
stock_return.head() - 1
title = str('Stock revenue since '+ str(start.date()))
stock_return.plot(grid = True,title = title).axhline(y = 1, color = "black", lw = 2)
plt.show()
## Classical Risk Metrics
