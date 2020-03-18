
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from utility.utils import *
import time
import os

plt.style.use('ggplot')

## INIT ##
try:
    os.remove("transactions.json")
    print("Clearing past transactions!")
except:
    pass
n = 5
cash = 12500
input_cash = []
shares = []
shares_price = []
for i in range(n):
    input_cash.append(cash/n)
    shares.append(0)
    shares_price.append(0)

## TRADING ##
tickers = []
print("Start trading with",cash,"$.")
while True:
    ## Phase 0: Gather data ##
    tickers = pullstockfrom_av(n,tickers)
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
