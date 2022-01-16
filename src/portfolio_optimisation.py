import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from finquant.portfolio import build_portfolio


def app():
    st.title('Portfolio Optimisation')
    try:
        weightings = st.session_state.weightings
        df_close = st.session_state.df_close
    except AttributeError:
        weightings = None
    if not weightings:
        st.write('Please build your portfolio first.')
        return
    d = {
        x: {"Name": name, "Allocation": allocation}
        for x, (name, allocation)
        in zip(range(len(weightings)), weightings.items())
    }
    pf_allocation = pd.DataFrame.from_dict(d, orient="index")
    pf_allocation['Allocation'] = pf_allocation['Allocation'].astype(float)
    try:
        pf = st.session_state.pf
        opt_w = st.session_state.opt_w
        opt_res = st.session_state.opt_res
    except AttributeError:
        pf, opt_w, opt_res = build_finquant_portfolio(df_close, pf_allocation)
    if not pf.portfolio.equals(pf_allocation):
        pf, opt_w, opt_res = build_finquant_portfolio(df_close, pf_allocation)

    st.header('Efficient Frontier')
    pf.mc_plot_results()
    pf.ef_plot_efrontier()
    pf.ef.plot_optimal_portfolios()
    # plotting individual stocks
    pf.plot_stocks()
    st.pyplot(plt)

    st.header('Optimal Weights by Optimisation Type')
    optimisation_type = st.selectbox(
        'Optimisation Type',
        opt_w.transpose().columns
    )
    st.plotly_chart(
        px.pie(
            opt_w.transpose(),
            names=opt_w.columns,
            values=optimisation_type
        )
    )

    st.header('Efficient Volatility')
    st.write('Find the portfolio with the maximum Sharpe Ratio for a given target Volatility')
    volatility = st.slider(
        'Volatility',
        min_value=float(opt_res.loc['Min Volatility', 'Volatility']),
        max_value=float(opt_res.loc['Max Sharpe Ratio','Volatility']),
        step=0.01,
    )
    st.plotly_chart(
        px.pie(
            pf.ef_efficient_volatility(volatility),
            names=pf.ef_efficient_volatility(volatility).index,
            values='Allocation'
        )
    )

    st.header('Efficient Expected Return')
    st.write('Find the portfolio with the minimum Volatility for a given target return.')
    exp_return = st.slider(
        'Expected Return',
        min_value=float(opt_res.loc['Min Volatility', 'Expected Return']),
        max_value=float(opt_res.loc['Max Sharpe Ratio','Expected Return']),
        step=0.01,
    )
    st.plotly_chart(
        px.pie(
            pf.ef_efficient_return(exp_return),
            names=pf.ef_efficient_return(exp_return).index,
            values='Allocation'
        )
    )


def build_finquant_portfolio(df, pf_allocation):
    pf = st.session_state.pf = build_portfolio(
        data=df,
        pf_allocation=pf_allocation
    )
    opt_w, opt_res = pf.mc_optimisation(num_trials=5000)
    st.session_state.opt_w = opt_w
    st.session_state.opt_res = opt_res

    return pf, opt_w, opt_res
