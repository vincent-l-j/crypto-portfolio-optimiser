#!/usr/bin/env python
# coding: utf-8

# # Crypto Portfolio Analysis

# In[1]:


# imports
import panel as pn
pn.extension('plotly')
import plotly.express as px
import pandas as pd
import hvplot.pandas
import matplotlib.pyplot as plt
from binance import Client


# In[2]:


# Initialize the Panel Extensions (for Plotly)
import panel as pn
pn.extension("plotly")

# Import panel.interact
from panel.interact import interact

# for merging the dataframes
from functools import reduce


# ## Instantiate the Binance API Client

# In[3]:


# Pulling price data doesn't require an api key as it is publicly available
# https://python-binance.readthedocs.io/en/latest/
# https://binance-docs.github.io/apidocs/spot/en/#compressed-aggregate-trades-list
client = Client()


# ## Get list of all cryptocurrencies traded on the Binance exchange
# 

# In[4]:


exchange_info = client.get_exchange_info()
symbols = exchange_info['symbols']
# Ensure no duplicates by using sets
coin_set = {s['baseAsset'] for s in symbols} | {s['quoteAsset'] for s in symbols}
coin_list = sorted(coin_set)


# ## Create a DataFrame of the closing prices and dates for each chosen cryptocurrency in the portfolio

# In[5]:


def get_historical_data(currency):
    klines = client.get_historical_klines(currency + 'USDT', Client.KLINE_INTERVAL_1DAY, "1 year ago UTC")
    # klines columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    df = pd.DataFrame(((x[0], x[4]) for x in klines), columns=['timestamp', currency])
    df[currency] = df[currency].astype(float)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    return df

# Chosen cryptocurrenies
crypto_portfolio = ('BTC', 'ETH', 'SOL')
# Global dataframe
df = reduce(lambda left,right: pd.merge(left,right,left_index=True, right_index=True, how='outer'), map(get_historical_data, crypto_portfolio))
df.head()


# - - -

# ## Panel Visualisation

# In[6]:


# Make your plot here

df_change = df.pct_change().dropna()

weights = [6/10, 2/10, 2/10]
portfolio_return = weights * df_change
portfolio_sum = portfolio_return.sum(axis=1)
portfolio_sum.head(10)

variance_btc = df_change['BTC'].var()
covariance_portfolio = portfolio_sum.cov(df_change['BTC'])
portfolio_beta = covariance_portfolio / variance_btc

rolling_variance = df_change['BTC'].rolling(window=30).var()
rolling_covariance = portfolio_sum.rolling(window=30).cov(df_change['BTC'])
rolling_beta = rolling_covariance / rolling_variance 


combined_df = pd.concat([df_change['BTC'], portfolio_sum], axis='columns', join='inner')

combined_df.rename(columns={
    combined_df.columns[1]: 'Portfolio', 
    combined_df.columns[0]: 'BTC'
}, inplace=True)

combined_df.index.rename('Time', inplace=True)

correlation = combined_df['BTC'].rolling(window=30).corr(combined_df['Portfolio'])

correlation.hvplot(figsize=(15,8), title='Portfolio Correlation to BTC', fontsize='12pt', color='green')


# In[7]:


rolling_beta.hvplot(figsize=(25,10), title='Rolling 30-Day Portfolio Beta', fontsize='12pt', color='red')

