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

### How has your portfolio performed cumulatively in the past year?

### How strongly correlated is your portfolio to BTC?

### How volatile is your portfolio?

### How might your portfolio perform in one year?

### What is the most probable expected portfolio return in one year?

### Calculate the efficient frontier
The efficient frontier is the set of optimal portfolios that offer the highest expected return for a defined level of risk or the lowest risk for a given level of expected return. Portfolios that lie below the efficient frontier are sub-optimal because they do not provide enough return for the level of risk.

![efficient_frontier](images/efficient_frontier.png)

### Find the portfolio with the minimum volatility
The efficient portfolio weightings with the maximum Sharpe Ratio:
| Asset | Weighting (%) |
|-------|---------------|
| BTC   | 95.2          |
| SOL   | 3.25          |
| ETH   | 1.56          |

![min_volatility](images/min_vol_weight.png)

### Find the portfolio with the maximum Sharpe Ratio, also called the tangency portfolio
The efficient portfolio weightings with the maximum Sharpe Ratio:
| Asset | Weighting (%) |
|-------|---------------|
| SOL   | 97.4          |
| BTC   | 2.46          |
| ETH   | 0.191         |

![max_sharpe_ratio](images/max_sharp_weight.png)

### Given a target volatility of 0.85, find the portfolio with the maximum Sharpe Ratio
The efficient portfolio weightings with a target volatility of 0.85 are:
| Asset | Weighting (%) |
|-------|---------------|
| SOL   | 49            |
| BTC   | 39.1          |
| ETH   | 12            |

![volatility_0.85](images/efficient_volatility_0.85.png)

### Given an expected return of 1.5, find the portfolio with the minimum volatility
The efficient portfolio weightings with an expected return of 1.5 are:
| Asset | Weighting (%) |
|-------|---------------|
| BTC   | 58.4          |
| SOL   | 36            |
| ETH   | 5.64          |

![return_1.5](images/efficient_expected_return_1.5.png)
