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
    """get most promising stocks by checking yahoo.finance.com for stocks with
       highest positive % change
    n is number of stocks
    """
    target_url= "https://finance.yahoo.com/gainers"

    sauce = urllib.request.urlopen(target_url).read()
    soup = bs.BeautifulSoup(sauce,features="html.parser")

    table = soup.table
    table_rows = table.find_all('tr')
    changes = []
    tickers = []
    for tr in table_rows:
        #print(tr)
        td = tr.find_all('td')
        #print(td)
        row = [ i.text for i in td]
        try:
            tickers.append(row[0])
            changes.append(row[4])
        except:
            continue
    return tickers[0:n]


def pullstockfrom_av(tickers):
    """pull intraday stock data to csv via alpha_vantage API
    tickers is list of stock tickers to be pulled
    """
    ts = TimeSeries(key='E9XI5UP9ZBAWPV84',output_format='pandas')
    # Get pd.dataframe with the intraday data and another with  the call's metadata
    for ticker in tickers:
        data, meta_data = ts.get_intraday(ticker,outputsize='compact',interval='1min')
        data.columns=["Open", "High", "Low", "Close",'Volume']
        path = os.path.join('C:/Users/David/Documents/Projekte/Davids_StockMarket/data/',ticker)
        data.to_csv(str(path)+'.csv')
    return

def pullstockfrom_av_long(tickers):
    """pull daily stock data to csv via alpha_vantage API
    tickers is list of stock tickers to be pulled
    """
    ts = TimeSeries(key='E9XI5UP9ZBAWPV84',output_format='pandas')
    # Get pd.dataframe with the intraday data and another with  the call's metadata
    for ticker in tickers:
        data, meta_data = ts.get_daily(ticker,outputsize='full')
        data.columns=["Open", "High", "Low", "Close",'Volume']
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
    close_stock_df = bollinger_bands(stock['Close'])
    plt.plot(close_stock_df['Close'],'black')
    plt.plot(close_stock_df['upper'],'orange')
    plt.plot(close_stock_df['lower'],'orange')
    plt.legend(['Close','upper','lower'])

    plt.title(('Intraday TimeSeries '+ ticker))
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
    print(time)
    ID = ticker+str(time)
    return buy,sell,price,ID
