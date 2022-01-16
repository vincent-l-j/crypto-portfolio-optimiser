import streamlit as st
import panel as pn
pn.extension('plotly')
import plotly.express as px
import pandas as pd
import hvplot.pandas
import matplotlib.pyplot as plt
from binance import Client
from MCForecastTools import MCSimulation

def app():
    st.title('Portfolio Forecasting')

    try:
        df_ohlcv = st.session_state.df_ohlcv
    except AttributeError:
        st.write('Please build your portfolio first.')
        return
    
    MC_traditional_dist = MCSimulation(
        portfolio_data = st.session_state.df_ohlcv,
        weights = [.60,.20,.20],
        num_simulation = 100,
        num_trading_days = 365*1
    )

    MC_traditional_dist.calc_cumulative_return()

st.pyplot(mc_line_plot(MC_tradititonal_dist))
st.pyplot(mc_dist_plot(MC_tradititonal_dist))
st.write(investment_return(MC_tradititonal_dist))

def mc_line_plot (mc):
   
    line_plot = mc.plot_simulation()
   
    return line_plot
    
def mc_dist_plot (mc):
    
    mc_dist_plot = mc.plot_distribution()
            
    return mc_dist_plot      


def investment_return (mc, initial_investment = 20000):
   
    traditional_tbl = mc.summarize_cumulative_return()
    ci_lower = round(traditional_tbl[8]*initial_investment,2)
    ci_upper = round(traditional_tbl[9]*initial_investment,2)

    return (f"There is a 95% chance that an initial investment of ${initial_investment:,} in the portfolio"
           f" over the next 12 months will end within the range of"
           f" ${ci_lower:,} and ${ci_upper:,}")
