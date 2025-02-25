import yfinance as yf
import pandas as pd

# List of selected stocks
stocks = ["MSFT", "AAPL", "KO", "GE", "JPM", "MMM"]

# Define time period
start_date = "1999-01-01"
end_date = "2024-12-31"

# Dictionary to store dataframes
stock_data = {}

# Fetch stock data from Yahoo Finance
for stock in stocks:
    print(f"Downloading data for {stock}...")
    ticker = yf.Ticker(stock)
    data = ticker.history(start=start_date, end=end_date, auto_adjust=True)
    stock_data[stock] = data

# Convert to DataFrame and save
all_data = pd.concat(stock_data, axis=1)
all_data.to_csv("stock_data_1999_2024.csv")

# Display first few rows
print(all_data.head())
