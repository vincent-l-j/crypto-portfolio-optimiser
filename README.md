# project-1

## Requirements
- [Anaconda](https://www.anaconda.com/products/individual)

## Installation
- Clone this repo
```
cd /path/to/project-1
conda create -n <your-env-name> python=3.9.5
conda activate <your-env-name>
pip install -r requirements.txt
streamlit run app.py
```

---

## Summary of Findings

This should include a heading for each question that was asked of your data, with a short description of what you found and any relevant plots under each heading.

The following analysis was performed using a chosen portfolio of [`BTC`, `ETH`, `SOL`] with weightings of [60, 20, 20] respectively.

### How has your portfolio performed in the past year?

![daily returns](daily_returns_plt.png)

### How has your portfolio performed cumulatively in the past year?

![cum_returns plot](https://github.com/vincent-l-j/project-1/blob/main/images/cum_returns_plt.png)

### How strongly correlated is your portfolio to BTC?

![corr plot](https://github.com/vincent-l-j/project-1/blob/main/images/corr_plt.png)

### How volatile is your portfolio?

![Beta Plot](https://github.com/vincent-l-j/project-1/blob/main/images/bet_plt.png)

### How might your portfolio perform in one year?

![monete carlo](https://github.com/vincent-l-j/project-1/blob/main/images/monte_carlo.png)

### What is the most probable expected portfolio return in one year?

![dis monte carlo](https://github.com/vincent-l-j/project-1/blob/main/images/dis_monte_carlo.png)

### Is the portfolio performing adequately?

![frontier](https://github.com/vincent-l-j/project-1/blob/main/images/efficient_frontier.png)

### Find the portfolio with the minimum volatility

![min vol](https://github.com/vincent-l-j/project-1/blob/main/images/min_vol_weight.png)

### Find the portfolio with the maximum Sharpe Ratio, also called the tangency portfolio

![max sharpe](https://github.com/vincent-l-j/project-1/blob/main/images/max_sharp_weight.png)

### Given a target volatility of 0.85, find the portfolio with the maximum Sharpe Ratio

![vol](https://github.com/vincent-l-j/project-1/blob/main/images/efficient_volatility_0.85.png)

### Given an expected return of 1.5, find the portfolio with the minimum volatility

![expected return](https://github.com/vincent-l-j/project-1/blob/main/images/efficient_expected_return_1.5.png)
