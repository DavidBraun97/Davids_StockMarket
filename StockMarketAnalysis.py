import pandas as pd
import datetime
import matplotlib.pyplot as plt
import time
import quandl

from utility.utils import *

plt.style.use('ggplot')


### INIT ###
tickers = ["AAPL","GOOG",'MSFT']
start = datetime.datetime(2016,1,1)
end = datetime.date.today()
n = len(tickers)
investment = 10000

##  Gather data ##
pullstockfrom_av_long(tickers,start)

for i in range(n):
    stock_df = getdffromcsv(tickers[i])
    print("\nAnalyzing ", tickers[i])
    ## Classical Risk Metrics
    SR = SharpRatio(stock_df.loc[:,['adj. Close']], 1.02)
    print('Sharp Ratio (risk free rate: 1.02): ', SR.round(3))

    trades_df = MA_Crossover(stock_df,tickers[i],investment)
    profit = calculateProfit(trades_df)
    print("Profit with stock",tickers[i],"between",str(start.date()),"and",str(end),":",profit.round(3))
