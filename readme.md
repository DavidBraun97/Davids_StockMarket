Throughout the past few months I became quite interested in finance, i.e. the stock market. Due to the covid-19 pandemic and the corresponding closure of university, I decided to use my additional free time to work on this fun little project:

**Please Note**: I am very much aware of the risks trading, especially daytrading, comes along. Neithertheless I wanted to build a little application that would trade automatically using **imaginary budget**.

Running the python script *AutomatedIntradayTrading.py* will make trades with up to 5 stocks concurrently. To this end, the market is monitored in real time at a frequency of 1 minutes.

Program Sequence:
  1) Check Yahoo.finance for promising stocks (based on the recent past % change)
  2) Pull live stock data using the alpha vantage API
  3) Based on a technical analysis, stocks are bought and selled automatically
  4) Bookkeeping  
