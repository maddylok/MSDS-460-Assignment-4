import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(filename='portfolio_performance.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load screened stocks
screened_stocks = pd.read_csv("screened_fundamental_data.csv", index_col=0)
selected_stocks = screened_stocks.index.tolist()

# Define time period
start_date = "1999-01-01"
end_date = "2024-12-31"

# Retrieve historical price data
price_data = yf.download(selected_stocks, start=start_date, end=end_date)["Close"]

# Retrieve dividend data
dividends = {}
for stock in selected_stocks:
    ticker = yf.Ticker(stock)
    dividends[stock] = ticker.dividends.resample("YE").sum()

dividend_df = pd.DataFrame(dividends).fillna(0)
dividend_df.index = dividend_df.index.tz_localize(None)

# Get year-end prices
year_end_prices = price_data.resample("YE").last()
year_end_prices.index = year_end_prices.index.tz_localize(None)

# Calculate dividend yield
dividend_yield = dividend_df / year_end_prices
dividend_yield.fillna(0, inplace=True)

# Compute equal-weighted portfolio returns (no rebalancing, with yearly dividend reinvestment)
portfolio_returns = price_data.pct_change().mean(axis=1)
portfolio_cumulative = (1 + portfolio_returns).cumprod()

# Save portfolio returns for Monte Carlo simulation
portfolio_returns.to_csv("portfolio_returns.csv")


# Apply dividend reinvestment yearly
reinvestment_factor = (1 + dividend_yield).prod(axis=1)

for date in reinvestment_factor.index:
    if date in portfolio_cumulative.index:
        reinvestment_adjustment = 1 + dividend_yield.loc[date].mean()
        portfolio_cumulative.loc[date:] *= reinvestment_adjustment

# Retrieve S&P 500 (SPY) for comparison
spy = yf.download("SPY", start=start_date, end=end_date)["Close"]
spy_returns = spy.pct_change()
spy_cumulative = (1 + spy_returns).cumprod()

# Performance Metrics Calculation
def annualized_return(returns):
    return (1 + returns.mean()) ** 252 - 1

def annualized_volatility(returns):
    return returns.std() * np.sqrt(252)

def sharpe_ratio(returns, risk_free_rate=0.02):
    return (annualized_return(returns) - risk_free_rate) / annualized_volatility(returns)

def max_drawdown(cumulative_returns):
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    return drawdown.min()

portfolio_annual_return = annualized_return(portfolio_returns)
portfolio_volatility = annualized_volatility(portfolio_returns)
portfolio_sharpe = sharpe_ratio(portfolio_returns)
portfolio_max_drawdown = max_drawdown(portfolio_cumulative)

spy_annual_return = annualized_return(spy_returns.dropna()).item()
spy_volatility = annualized_volatility(spy_returns.dropna()).item()
spy_sharpe = sharpe_ratio(spy_returns.dropna()).item()
spy_max_drawdown = max_drawdown(spy_cumulative.dropna()).item()

# Log performance metrics
logging.info("Portfolio Performance Metrics:")
logging.info(f"Annualized Return: {portfolio_annual_return:.2%}")
logging.info(f"Annualized Volatility: {portfolio_volatility:.2%}")
logging.info(f"Sharpe Ratio: {portfolio_sharpe:.2f}")
logging.info(f"Max Drawdown: {portfolio_max_drawdown:.2%}")

logging.info("\nS&P 500 Performance Metrics:")
logging.info(f"Annualized Return: {spy_annual_return:.2%}")
logging.info(f"Annualized Volatility: {spy_volatility:.2%}")
logging.info(f"Sharpe Ratio: {spy_sharpe:.2f}")
logging.info(f"Max Drawdown: {spy_max_drawdown:.2%}")

# Print performance metrics
print("Portfolio Performance Metrics:")
print(f"Annualized Return: {portfolio_annual_return:.2%}")
print(f"Annualized Volatility: {portfolio_volatility:.2%}")
print(f"Sharpe Ratio: {portfolio_sharpe:.2f}")
print(f"Max Drawdown: {portfolio_max_drawdown:.2%}")

print("\nS&P 500 Performance Metrics:")
print(f"Annualized Return: {spy_annual_return:.2%}")
print(f"Annualized Volatility: {spy_volatility:.2%}")
print(f"Sharpe Ratio: {spy_sharpe:.2f}")
print(f"Max Drawdown: {spy_max_drawdown:.2%}")

# Plot Portfolio vs. S&P 500
plt.figure(figsize=(12, 6))
plt.plot(portfolio_cumulative, label="Market-Cap Weighted Portfolio (With Dividend Reinvestment)")
plt.plot(spy_cumulative, label="S&P 500 (SPY)", linestyle='dashed')
plt.legend()
plt.title("Portfolio vs. S&P 500 Performance (No Rebalancing, With Yearly Dividend Reinvestment)")
plt.xlabel("Year")
plt.ylabel("Cumulative Returns")
plt.show()
