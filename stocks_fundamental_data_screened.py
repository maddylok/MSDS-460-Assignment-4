import yfinance as yf
import pandas as pd

# List of selected stocks
stocks = ["MMM", "ABT", "ABBV", "ACN", "MO", "AMGN", "ADM", "T", "BAC", "BAX", "BDX", "BLK", "BA", "BMY", "CAH", "CAT", "CVX", "CSCO", "CLX", "COKE", "CL", "CAG", "ED", "COST", "CMI", "DE", "DOV", "DUK", "ETN", "EMR", "EXC", "XOM", "FRT", "FDX", "FSLR", "FL", "F", "BEN", "GD", "GE", "GIS", "GM", "GPC", "GILD", "GS", "GGG", "HRB", "HAS", "HSY", "HON", "HRL", "IBM", "ITW", "IR", "INTC", "IBM", "IFF", "JNJ", "JPM", "K", "KMB", "KHC", "KR", "LEG", "LLY", "LMT", "LOW", "MTB", "M", "MAR", "MMC", "MCD", "MDT", "MRK", "MET", "MSFT", "MDLZ", "MS", "MSI", "NEE", "NKE", "NSC", "NOC", "NUE", "OXY", "OMC", "PH", "PEP", "PFE", "PM", "PPG", "PG", "PRU", "PEG", "QCOM", "RTX", "O", "RF", "RHI", "ROK", "ROP", "SPGI", "CRM", "SHW", "SPG", "SO", "SWK", "SBUX", "STT", "SYY", "TROW", "TGT", "TXN", "HD", "TRV", "DIS", "TMO", "TJX", "TSCO", "TFC", "TSN", "USB", "UNP", "UPS", "UNH", "VLO", "VZ", "WBA", "WMT", "WM", "WFC", "WST", "WY", "WHR", "WMB", "GWW", "XEL"]

# Define fundamental metrics to retrieve
fundamental_data = {}

for stock in stocks:
    print(f"Fetching data for {stock}...")
    ticker = yf.Ticker(stock)
    
    # Retrieve key financials
    fundamentals = {
        "Market Cap": ticker.info.get("marketCap"),
        "P/E Ratio": ticker.info.get("trailingPE"),
        "P/B Ratio": ticker.info.get("priceToBook"),
        "ROE": ticker.info.get("returnOnEquity"),
        "ROA": ticker.info.get("returnOnAssets"),
        "Debt/Equity": ticker.info.get("debtToEquity"),
        "Dividend Yield": ticker.info.get("dividendYield"),
        "Payout Ratio": ticker.info.get("payoutRatio"),
        "Revenue Growth": ticker.info.get("revenueGrowth"),
        "Earnings Growth": ticker.info.get("earningsGrowth")
    }
    
    fundamental_data[stock] = fundamentals

# Convert to DataFrame
fundamental_df = pd.DataFrame(fundamental_data).T

# Define screening criteria
screened_df = fundamental_df[
    (fundamental_df["P/E Ratio"].between(5, 100, inclusive='both')) &
    (fundamental_df["P/B Ratio"] <= 10) &
    (fundamental_df["ROE"] > 0) &
    (fundamental_df["ROA"] > 0) &
    (fundamental_df["Debt/Equity"] <= 100) &
    (fundamental_df["Dividend Yield"] >= 0.5) &
    (fundamental_df["Payout Ratio"] <= 1) &
    (fundamental_df["Revenue Growth"] > 0) &
    (fundamental_df["Earnings Growth"] > 0)
]

# Save results to CSV
screened_df.to_csv("screened_fundamental_data.csv")

# Display screened stocks
print("Filtered Stocks Based on Fundamental Screening:")
print(screened_df)
