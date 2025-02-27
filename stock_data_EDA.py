import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
all_data = pd.read_csv("stock_data_1999_2024.csv", header=[0, 1], index_col=0, parse_dates=True)

# Ensure index is in datetime format with UTC handling
all_data.index = pd.to_datetime(all_data.index, utc=True)

# Extract adjusted close prices
adj_close = all_data.xs('Close', axis=1, level=1)

# Compute monthly log returns
monthly_returns = 100 * np.log(adj_close.resample('ME').last() / adj_close.resample('ME').first())

# Summary statistics
summary_stats = monthly_returns.describe()
print(summary_stats)

# Plot adjusted closing prices
plt.figure(figsize=(12, 6))
plt.axes([0.08, 0.1, 0.6, 0.8])
for stock in adj_close.columns:
    plt.plot(adj_close.index, adj_close[stock], label=stock)
plt.title("Stock Price Trends (1999-2024)")
plt.xlabel("Year")
plt.ylabel("Adjusted Close Price")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., ncol=4, prop={'size': 8})
plt.show()

# Plot return distributions
plt.figure(figsize=(12, 6))
plt.axes([0.08, 0.1, 0.6, 0.8])
for stock in monthly_returns.columns:
    sns.kdeplot(monthly_returns[stock].dropna(), label=stock)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., ncol=4, prop={'size': 8})
plt.title("Stock Monthly Return Distributions")
plt.xlabel("Log Return")
plt.ylabel("Density")
plt.show()

# Compute rolling volatility
rolling_vol = monthly_returns.rolling(window=12).std() * np.sqrt(12)

# Plot rolling volatility
plt.figure(figsize=(12, 6))
plt.axes([0.08, 0.1, 0.6, 0.8])
for stock in rolling_vol.columns:
    plt.plot(rolling_vol.index, rolling_vol[stock], label=stock)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., ncol=4, prop={'size': 8})
plt.title("Rolling Volatility (12-month window)")
plt.xlabel("Year")
plt.ylabel("Annualized Volatility")
plt.show()
