Throughout the past few months I became quite interested in finance, i.e. the stock market. Due to the covid-19 pandemic and the corresponding closure of university, I decided to use my additional free time to work on this fun little project:

**Please Note**: I am very much aware of the risks trading, especially daytrading, comes along. Neithertheless I wanted to build a little application that would trade automatically using **imaginary budget**.

Below the rough functionality is given:
Running the python script *AutomatedIntradayTrading.py* will do the follwing.

1) Check Yahoo.finance for promising stocks (based on the recent past % change)
while true (1 min frequency)
  2) Pull live stock data using the alpha vantage API
  3) Based on a technical analysis, stocks are bought and selled automatically
  4) Bookkeeping  
