#!/usr/bin/env python
# coding: utf-8

# # Volume-Weighted Moving Average (VWMA) 

# https://www.tradingsetupsreview.com/volume-weighted-moving-average-vwma/

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import yfinance as yf
yf.pdr_override()
import datetime as dt

# input
symbol = 'AAPL'
start = dt.date.today() - dt.timedelta(days = 180)
end = dt.date.today()

# Read data 
df = yf.download(symbol,start,end)
start = '2018-12-01'
end = '2019-02-01'

# Read data 
df = yf.download(symbol,start,end)

import talib as ta


df['SMA'] = ta.SMA(df['Adj Close'], timeperiod=3)

df['VWMA'] = ((df['Adj Close']*df['Volume'])+(df['Adj Close'].shift(1)*df['Volume'].shift(1))+(df['Adj Close'].shift(2)*df['Volume'].shift(2))) / (df['Volume'].rolling(3).sum())
df.head()

def VWMA(close,volume, n):
    cv =pd.Series(close.shift(n) * volume.shift(n))
    tv = volume.rolling(n).sum()
    vwma = cv/tv
    return vwma

VWMA(df['Adj Close'],df['Volume'], 3)


# In[37]:


plt.figure(figsize=(14,8))
plt.plot(df['Adj Close'])
plt.plot(df['VWMA'], label='Volume Weighted Moving Average')
plt.plot(df['SMA'], label='Simple Moving Average')
plt.legend(loc='best')
plt.title('Stock of Midpoint Method')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()


# ## Candlestick with VWMA

# In[38]:


from matplotlib import dates as mdates

dfc = df.copy()
dfc['VolumePositive'] = dfc['Open'] < dfc['Adj Close']
#dfc = dfc.dropna()
dfc = dfc.reset_index()
dfc['Date'] = mdates.date2num(dfc['Date'].astype(dt.date))
dfc.head()


# In[40]:


from mplfinance.original_flavor import candlestick_ohlc

fig = plt.figure(figsize=(14,7))
ax1 = plt.subplot(2, 1, 1)
candlestick_ohlc(ax1,dfc.values, width=0.5, colorup='g', colordown='r', alpha=1.0)
ax1.plot(df['VWMA'], label='Volume Weighted Moving Average')
ax1.plot(df['SMA'], label='Simple Moving Average')
ax1.set_title('Stock '+ symbol +' Closing Price')
ax1.set_ylabel('Price')
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
ax1.grid(True, which='both')
ax1.minorticks_on()
ax1v = ax1.twinx()
colors = dfc.VolumePositive.map({True: 'g', False: 'r'})
ax1v.bar(dfc.Date, dfc['Volume'], color=colors, alpha=0.4)
ax1v.axes.yaxis.set_ticklabels([])
ax1v.set_ylim(0, 3*df.Volume.max())
ax1.set_title('Stock '+ symbol +' Closing Price')
ax1.set_ylabel('Price')
ax1.legend(loc='best')

