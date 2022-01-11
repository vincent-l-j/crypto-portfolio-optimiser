import streamlit as st

def app():
    # Create a Title for the Dashboard
    dashboard_title = 'Crypto Portfolio Analysis'

    # Define a welcome text
    welcome_text = (
        'This dashboard presents a visual analysis of historical performance of cryptocurrencies. '
        'You can navigate through the sidebar tabs to explore more details about '
        'possible portfolios and Montecarlo simulations.'
    )

    st.title(dashboard_title)

    st.write(welcome_text)
