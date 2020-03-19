import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import json
import os
import urllib.request
import bs4 as bs

from alpha_vantage.timeseries import TimeSeries
plt.style.use('ggplot')

##### UTILITY FUNCTIONS #####

def getpromisingstocks(n):
    """get most promising stocks by checking https://tradingeconomics.com for
    stocks with highest positive % change
    n is number of stocks
    """
    target_url= "https://tradingeconomics.com/united-states/stock-market"

    sauce = urllib.request.urlopen(target_url).read()
    soup = bs.BeautifulSoup(sauce,features="html.parser")

    table = soup.findAll('table')[1]
    table_rows = table.find_all('tr')
    changes = []
    tickers = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [ i.text for i in td]
        try:
            ticker = row[0]
            ticker = ticker.replace('\n', '')
            tickers.append(ticker)
            changes.append(row[5])
        except:
            pass
    df = pd.DataFrame({'Tickers':tickers,'%Changes':changes})
    df.sort_values(by=['%Changes'],ascending=False,inplace=True)
    return tickers[0:n]


def pullstockfrom_av(n,tickers):
    """pull intraday stock data to csv via alpha_vantage API
    n is number of stocks concurrently traded
    """
    ts = TimeSeries(key='E9XI5UP9ZBAWPV84',output_format='pandas')
    if tickers == []:
        tickers = getpromisingstocks(n)
        prom_tickers = []
        print("Checking for most promising stocks.")
    else:
        prom_tickers = tickers
    # Get pd.dataframe with the intraday data and another with  the call's metadata
    for i in range(n):
        try:
            data, meta_data = ts.get_intraday(tickers[i],outputsize='compact',interval='1min')
            data.columns=["Open", "High", "Low", "Close",'Volume']
            path = os.path.join('C:/Users/David/Documents/Projekte/Davids_StockMarket/data/',tickers[i])
            data.to_csv(str(path)+'.csv')
            prom_tickers.append(tickers[i])
        except:
            print(tickers[i], " not available on alpha_vantage. It is substituted by ", tickers[i+1])
    return prom_tickers

def pullstockfrom_av_long(tickers,start):
    """pull daily stock data to csv via alpha_vantage API
    tickers is list of stock tickers to be pulled
    """
    ts = TimeSeries(key='E9XI5UP9ZBAWPV84',output_format='pandas')
    # Get pd.dataframe with the intraday data and another with  the call's metadata
    for ticker in tickers:
        data, meta_data = ts.get_daily_adjusted(ticker,outputsize='full')
        data.columns=["Open", "High", "Low", "Close", 'adj. Close','Volume','dividend amount','split coefficient']
        keep = data.index >= start
        data = data[keep]
        path = os.path.join('C:/Users/David/Documents/Projekte/Davids_StockMarket/data/',ticker)
        data.to_csv(str(path)+'.csv')
    return

def getdffromcsv(ticker):
    """get pd.dataframe from stored csv tables
    ticker is stock ticker (string)
    """
    path = os.path.join('C:/Users/David/Documents/Projekte/Davids_StockMarket/data/',ticker)
    df = pd.read_csv(str(path)+'.csv',index_col = 'date')
    df.index=pd.to_datetime(df.index)
    return df
def candlestick_ohlc(stock_df,stockname):
    mpf.plot(stock_df,type='candle',title=stockname+' candlestick plot',show_nontrading=True,volume=True)
    return
def bollinger_bands(s, k=2, n=10):
    """get_bollinger_bands DataFrame
    s is series of values
    k is multiple of standard deviations
    n is rolling window
    """
    b = pd.concat([s, s.rolling(n,center=False).agg([np.mean, np.std]).shift(-n)], axis=1)
    b['upper'] = b['mean'] + b['std'] * k
    b['lower'] = b['mean'] - b['std'] * k

    return b.drop('std', axis=1)

def visualize_stocks_individually(stock, ticker):
    close_stock_df = bollinger_bands(stock['adj. Close'])
    plt.subplot(2,1,1)
    plt.plot(close_stock_df['adj. Close'],'black')
    plt.plot(close_stock_df['upper'],'orange')
    plt.plot(close_stock_df['lower'],'orange')
    plt.legend(['Adj. Close','upper','lower'])
    plt.title(('Adj. Close Prices with boellinger bands '+ ticker))
    plt.subplot(2,1,2)
    plt.plot(close_stock_df['adj. Close'],'black')
    plt.plot(close_stock_df['adj. Close'].rolling(window = 20, center = False).mean().shift(-20),'orange')
    plt.plot(close_stock_df['adj. Close'].rolling(window = 50, center = False).mean().shift(-20),'red')
    plt.plot(close_stock_df['adj. Close'].rolling(window = 200, center = False).mean().shift(-200),'green')

    plt.title(('Adj. Close Prices of '+ ticker))
    plt.legend(['Adj. Close','20d mean','50d mean','200d mean'])
    plt.show()
    return

def writetoJSON(ticker,buy,sell,hold,price,ID):
    """Bookkeeping: store transactions in json
    """
    try:
        data = json.load(open('transactions.json'))
    except:
        with open('transactions.json', 'w') as outfile:
            json.dump([],outfile)
        outfile.close() # Close the JSON file
        data = json.load(open('transactions.json'))
    if buy == True:
        newdata = {}
        newdata[ID] = []
        newdata[ID].append({
            'stock': ticker,
            'holding': hold,
            'bought for': price,
        })
        # convert data to list if not
        if type(data) is dict:
            data = [data]
        # append new item to data list
        data.append(newdata)

        # write list to file
        with open('transactions.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
    elif sell == True:
        newdata = {}
        newdata[ID] = []
        newdata[ID].append({
            'stock': ticker,
            'holding': hold,
            'sold for': price
        })
        # convert data to list if not
        if type(data) is dict:
            data = [data]
        # append new item to data list
        data.append(newdata)

        # write list to file
        with open('transactions.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
    return

def analyse_stock(stock_df,ticker,hold,share_price):
    """find trade opportunities through technical analysis
    stock_df is pd.DataFrame
    ticker is stock ticker (string)
    hold is number of stocks that are curr. hold
    share_price is pricce at which hold stocks have been purchased
    """
    close_stock_df = bollinger_bands(stock_df['Close'])
    idx_high  = close_stock_df['Close'] > close_stock_df['upper']

    price = close_stock_df['Close']
    price = price[0]

    profit_reached = price >= share_price*1.01

    if idx_high[0] == True and hold == 0:
        buy = True
        sell = False
    elif (idx_high[0] == False and hold > 0) or (profit_reached and hold > 0):
        buy = False
        sell = True
    else:
        buy = False
        sell = False
        price = 0
    time = close_stock_df.index[0]
    ID = ticker + str(time)
    return buy,sell,price,ID

def SharpRatio(stock_df, rf_rate):
    """calculate the Sharp Ratio
    stock_df is pd.Series
    rf_rate is return of risk free investment
    """
    stock_return = stock_df.apply(lambda x: x / x[-1])
    stockreturn_std = stock_return.std()
    SR = (stock_return.iloc[0,-1] - rf_rate)/stockreturn_std
    return np.float(SR)

def AlphaBeta():
    """calculate the alpha & beta
    tba
    """
    pass
    return [],[]
def MA_Crossover(stock_df,ticker,budget):
    """ Strategy: 'Moving average crossover' Strategy
    Upward momentum is confirmed with a bullish crossover, which occurs when a
    short-term moving average crosses above a longer-term moving average.
    Downward momentum is confirmed with a bearish crossover, which occurs when a
    short-term moving average crosses below a longer-term moving average.
    """
    stock_df["20d mean"] = stock_df['adj. Close'].rolling(window = 20, center = False).mean().shift(-20)
    stock_df["50d mean"] = stock_df['adj. Close'].rolling(window = 50, center = False).mean().shift(-50)

    stock_df["20d-50d"] = stock_df["20d mean"] - stock_df["50d mean"]
    stock_df["Regime"] = np.where(stock_df['20d-50d'] > 0, 1, 0)

    trigger = []
    shares = []
    p_old = 0
    iter = len(stock_df["Regime"])
    hold = 0
    for i in range(iter):
        p = stock_df["Regime"][iter-1-i]
        if p > 0 and p_old == 0:
            hold = budget//stock_df["adj. Close"][iter-1-i]
            trigger.append(1)
            p_old = 1
            budget = budget - hold*stock_df["adj. Close"][iter-1-i]
            shares.append(hold)
        elif p == 0 and p_old == 1:
            trigger.append(-1)
            p_old = 0
            budget = budget + hold*stock_df["adj. Close"][iter-1-i]
            shares.append(-hold)
            hold = 0
        else:
            trigger.append(0)
            shares.append(hold)

    stock_df["Trigger"] = trigger[::-1]
    stock_df["Shares"] = shares[::-1]
    # plt.plot(stock_df["Trigger"],'red')
    # plt.plot(stock_df['adj. Close'],'black')
    # plt.plot(stock_df['adj. Close'].rolling(window = 20, center = False).mean().shift(-20),'orange')
    # plt.plot(stock_df['adj. Close'].rolling(window = 50, center = False).mean().shift(-50),'green')
    # plt.show()

    prices = stock_df['adj. Close'][stock_df["Trigger"] != 0]
    trigger = stock_df['Trigger'][stock_df["Trigger"] != 0]
    shares = stock_df['Shares'][stock_df["Trigger"] != 0]
    trades_df = pd.concat([pd.DataFrame({'prices':prices}),pd.DataFrame({'indicator':trigger, 'shares':shares})],axis=1)

    iter = len(trades_df)
    profit= []
    for i in range(iter):
        if trades_df["indicator"][iter-1-i] == -1:
            profit_i = -trades_df["prices"][iter-i] + trades_df["prices"][iter-1-i]
        else:
            profit_i = 0
        profit.append(profit_i)
    trades_df['profit'] =  profit[::-1]
    print(trades_df)
    return trades_df

def calculateProfit(trades_df):
    """Calculates the profit per stock, considering transaction cost of 0.25%. """
    profit = (-trades_df["profit"]*trades_df["shares"]).sum()*0.995
    return profit
