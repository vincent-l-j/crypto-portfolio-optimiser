import streamlit as st
import pandas as pd
import hvplot.pandas
import holoviews as hv
import matplotlib.pyplot as plt
from .MCForecastTools import MCSimulation
import numpy as np

def app():
    st.title('Portfolio Forecasting')

    try:
        weightings = st.session_state.weightings
        df_ohlcv = st.session_state.df_ohlcv
    except AttributeError:
        weightings = None
    if not weightings:
        st.write('Please build your portfolio first.')
        return

    v = list(st.session_state.weightings.values())
    MC_traditional_dist = MCSimulation(
        portfolio_data = st.session_state.df_ohlcv,
        weights = v/np.linalg.norm(v),
        num_simulation = 100,
        num_trading_days = 365*1
    )

    try:
        old_mc_sim = st.session_state.MC_traditional_dist
    except AttributeError:
        old_mc_sim = None
    is_portfolio_different = (
        old_mc_sim is None
        or any(
            x != y
            for x,y in
            zip(
                MC_traditional_dist.portfolio_data.columns.get_level_values(0).unique(),
                old_mc_sim.portfolio_data.columns.get_level_values(0).unique(),
            )
        )
        or any(x != y for x,y in zip(MC_traditional_dist.weights, old_mc_sim.weights))
    )
    if is_portfolio_different:
        MC_traditional_dist.calc_cumulative_return()
        st.session_state.MC_traditional_dist = MC_traditional_dist
    MC_traditional_dist = st.session_state.MC_traditional_dist

    st.bokeh_chart(hv.render(mc_line_plot(MC_traditional_dist), backend='bokeh'))
    st.pyplot(mc_dist_plot(MC_traditional_dist))
    st.write(investment_return(MC_traditional_dist))

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
           f" over the next 1 year will end within in the range of"
           f" ${ci_lower:,} and ${ci_upper:,}")
