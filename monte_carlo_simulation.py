import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Load portfolio return data from the main script
portfolio_returns = pd.read_csv("portfolio_returns.csv", index_col=0, parse_dates=True).squeeze()

# Monte Carlo Simulation Parameters
num_simulations = 10000  # Number of Monte Carlo runs
num_days = 252 * 10  # Simulate 10 years of daily returns
initial_investment = 10000  # Starting portfolio value

# Calculate portfolio statistics
daily_mean_return = portfolio_returns.mean()
daily_volatility = portfolio_returns.std()

# Generate Monte Carlo simulations
simulated_portfolios = np.zeros((num_days, num_simulations))

for i in range(num_simulations):
    simulated_returns = np.random.normal(daily_mean_return, daily_volatility, num_days)
    simulated_portfolios[:, i] = initial_investment * (1 + simulated_returns).cumprod()

# Compute Statistics
final_values = simulated_portfolios[-1, :]
mean_final_value = np.mean(final_values)
median_final_value = np.median(final_values)
var_95 = np.percentile(final_values, 5)

# Plot Histogram of Final Portfolio Values
plt.figure(figsize=(12, 6))
plt.hist(final_values, bins=50, color="blue", alpha=0.7, edgecolor='black')
plt.axvline(mean_final_value, color='r', linestyle='dashed', linewidth=2, label=f'Mean: ${mean_final_value:,.2f}')
plt.axvline(median_final_value, color='g', linestyle='dashed', linewidth=2, label=f'Median: ${median_final_value:,.2f}')
plt.axvline(var_95, color='orange', linestyle='dashed', linewidth=2, label=f'95% VaR: ${var_95:,.2f}')
plt.title("Monte Carlo Simulation - Final Portfolio Value Distribution")
plt.xlabel("Final Portfolio Value ($)")
plt.ylabel("Frequency")
plt.legend()
plt.show()

# Print Simulation Summary
print(f"Mean Portfolio Value After 10 Years: ${mean_final_value:,.2f}")
print(f"Median Portfolio Value After 10 Years: ${median_final_value:,.2f}")
print(f"95% VaR (Worst 5% Outcome): ${var_95:,.2f}")

# Save Results
pd.DataFrame(final_values, columns=["Final Portfolio Value"]).to_csv("monte_carlo_results.csv", index=False)
