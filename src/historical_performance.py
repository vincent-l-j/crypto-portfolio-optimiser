import streamlit as st
import holoviews as hv
import pandas as pd

def app():
    st.title('Historical Performance')
    df_daily_returns = st.session_state.df_daily_returns
    df_daily_returns_plt = df_daily_returns.hvplot(figsize=(25,10), xlabel="Year", ylabel="Percentage change", title="Daily Returns over 1 Year")
    cumulative_returns = (1 + df_daily_returns).cumprod() - 1
    cum_returns_plt = cumulative_returns.hvplot(figsize=(25,10), xlabel="Year", ylabel="Percentage change", title="Cumulative Returns over 1 Year")
    st.bokeh_chart(hv.render(df_daily_returns_plt, backend='bokeh'))
    st.bokeh_chart(hv.render(cum_returns_plt, backend='bokeh'))