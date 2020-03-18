import pandas as pd
import datetime
import matplotlib.pyplot as plt
import time

from utility.utils import *

plt.style.use('ggplot')


##  Gather data ##
tickers = ["AAPL","GOOG",'MSFT']
#print("##  Pulling live stock data.  ##")
#pullstockfrom_av_long(tickers)

for ticker in tickers:
    stock_df = getdffromcsv(ticker)
    visualize_stocks_individually(stock_df, ticker)

aapl_df = getdffromcsv("AAPL")
goog_df = getdffromcsv("GOOG")
msft_df = getdffromcsv("MSFT")
stocks_df = pd.DataFrame({'APPL Close': aapl_df['Close'], 'GOOG Close': goog_df['Close'], 'MSFT Close': msft_df['Close']})
print(stocks_df.head(5))
stocks_df.plot(grid = True)
plt.show()
