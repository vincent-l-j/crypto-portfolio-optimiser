"""
This multi-page app was based on the [streamlit-multiapps](https://github.com/upraneelnihar/streamlit-multiapps) framework developed by [Praneel Nihar](https://medium.com/@u.praneel.nihar)
and his [Medium article](https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4).
"""
from src.multiapp import MultiApp
from src import (
    home,
    build_portfolio,
    historical_performance,
    beta_correlation,
    portfolio_forecasting,
    portfolio_optimisation,
    summary,
)

app = MultiApp()

# Add all your apps here
app.add_app("Home", home.app)
app.add_app("Build Your Portfolio", build_portfolio.app)
app.add_app("Historical Performance", historical_performance.app)
app.add_app("Beta & Correlation", beta_correlation.app)
app.add_app("Portfolio Forecasting", portfolio_forecasting.app)
app.add_app("Portfolio Optimisation", portfolio_optimisation.app)
app.add_app("Summary", summary.app)
# The main app
app.run()
