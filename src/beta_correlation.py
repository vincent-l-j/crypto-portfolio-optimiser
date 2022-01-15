import streamlit as st
import pandas as pd
import holoviews as hv
import numpy as np

#Beta and Correlation Portfolio App
def app():
    st.title('Portfolio Statistics')

    df_change = st.session_state.df_daily_returns

    v = list(st.session_state.weightings.values())
    weights = v/np.linalg.norm(v)
    portfolio_return = weights * df_change
    portfolio_sum = portfolio_return.sum(axis=1)

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
    #Correlation Plot
    correlation_plot = correlation.hvplot(figsize=(25,10), title='Portfolio Correlation to BTC', fontsize='12pt', color='green')
    st.bokeh_chart(hv.render(correlation_plot, backend='bokeh'))
    #Beta
    beta_plot = rolling_beta.hvplot(figsize=(25,10), title='Rolling 30-Day Portfolio Beta', fontsize='12pt', color='red')
    st.bokeh_chart(hv.render(beta_plot, backend='bokeh'))