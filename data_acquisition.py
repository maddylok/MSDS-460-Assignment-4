import yfinance as yf
import pandas as pd

# List of selected stocks
stocks = ["MMM", "ABT", "ABBV", "ACN", "MO", "AMGN", "ADM", "T", "BAC", "BAX", "BDX", "BLK", "BA", "BMY", "CAH", "CAT", "CVX", "CSCO", "CLX", "COKE", "CL", "CAG", "ED", "COST", "CMI", "DE", "DOV", "DUK", "ETN", "EMR", "EXC", "XOM", "FRT", "FDX", "FSLR", "FL", "F", "BEN", "GD", "GE", "GIS", "GM", "GPC", "GILD", "GS", "GGG", "HRB", "HAS", "HSY", "HON", "HRL", "IBM", "ITW", "IR", "INTC", "IBM", "IFF", "JNJ", "JPM", "K", "KMB", "KHC", "KR", "LEG", "LLY", "LMT", "LOW", "MTB", "M", "MAR", "MMC", "MCD", "MDT", "MRK", "MET", "MSFT", "MDLZ", "MS", "MSI", "NEE", "NKE", "NSC", "NOC", "NUE", "OXY", "OMC", "PH", "PEP", "PFE", "PM", "PPG", "PG", "PRU", "PEG", "QCOM", "RTX", "O", "RF", "RHI", "ROK", "ROP", "SPGI", "CRM", "SHW", "SPG", "SO", "SWK", "SBUX", "STT", "SYY", "TROW", "TGT", "TXN", "HD", "TRV", "DIS", "TMO", "TJX", "TSCO", "TFC", "TSN", "USB", "UNP", "UPS", "UNH", "VLO", "VZ", "WBA", "WMT", "WM", "WFC", "WST", "WY", "WHR", "WMB", "GWW", "XEL"]

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
