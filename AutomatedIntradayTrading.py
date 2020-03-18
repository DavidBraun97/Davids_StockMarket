
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from utility.utils import *
import time
plt.style.use('ggplot')

## INIT ##
tickers = getpromisingstocks(5)
n = len(tickers)
cash = 12500
input_cash = []
shares = []
shares_price = []
for i in range(n):
    input_cash.append(cash/n)
    shares.append(0)
    shares_price.append(0)

## TRADING ##
print("Start trading with ",cash,"$.\nConsidering ", tickers," stocks.\n\n")
while True:
    ## Phase 0: Gather data ##
    pullstockfrom_av(tickers)
    print("##  Pulling live stock data.  ##")
    for i in range(n):
        ticker = tickers[i]
        input = input_cash[i]
        hold = shares[i]
        share_price = shares_price[i]
        print('Looking for trade with ',ticker,' stocks.\nCurrently holding ',hold,' shares of',ticker, '.\nRemaining cash to be allocated in this period: ', input,'$')
        stock_df = getdffromcsv(ticker)
        ## Phase 1: Analyse Data and trade ##
        buy,sell,price,ID = analyse_stock(stock_df,ticker,hold,share_price)
        ##  Phase 3: Bookkeeping ##
        if buy:
            newshares = input//price
            hold = hold + newshares
            input = input%price
            share_price = price
            print('-> Buying ',newshares,' shares.')
        elif sell:
            soldshares = hold
            input = input + hold*price
            hold = 0
            share_price = 0
            print('-> Selling ',soldshares, ' shares.')
        else:
            print('-> No trade opportunity found in this period.')
        shares[i] = hold
        input_cash[i] = input
        shares_price[i] = share_price
        print('Currently holding ',hold,' shares of ',ticker, ' bought for',share_price,'.\nRemaining cash to be allocated in next period: ', input,'$\n')
        writetoJSON(ticker,buy,sell,hold,price,ID)

    time.sleep(60)
