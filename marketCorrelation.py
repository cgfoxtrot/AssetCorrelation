import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

def max_and_avg_divergence(data1, data2):
    difference = data1 - data2
    max_diff = difference.abs().max()
    avg_diff = difference.abs().mean()
    return max_diff, avg_diff

def interpret_correlation(correlation):
    if correlation is None or pd.isna(correlation):
        return "nan", "There is no consistent relationship between the movements of the two assets."
    elif correlation > 0:
        return "{:.2f} (positive)".format(correlation), "Typically, when one asset goes up, the other also tends to go up, and vice versa."
    elif correlation < 0:
        return "{:.2f} (negative)".format(correlation), "Generally, when one asset increases, the other tends to decrease, and vice versa. They move in opposite directions."

def analyze_assets_correlation():
    print("Welcome to the Asset Correlation Analyzer!")
    print("------------------------------------------------")
    print("This script allows you to analyze the correlation")
    print("and divergence between two financial assets.")
    print("It provides the following analyses:")
    print("1. Daily, 7-Day, and Monthly Correlations")
    print("2. Maximum and Average Divergences")
    print("------------------------------------------------")
    print("Example Symbols:")
    print("Dollar Index: DX-Y.NYB")
    print("S&P 500: ^GSPC")
    print("NASDAQ Composite: ^IXIC")
    print("Gold: GC=F")
    print("Crude Oil: CL=F")
    print("Apple Inc.: AAPL")
    print("Microsoft Corporation: MSFT")
    print("------------------------------------------------")

    # User input for ticker symbols
    asset1_ticker = input("Enter the first ticker symbol: ")
    asset2_ticker = input("Enter the second ticker symbol: ")

    # Define the time range
    end_date = datetime.now()
    start_date_year = end_date - timedelta(days=365)
    start_date_day = end_date - timedelta(days=1)

    # Fetch data using yfinance
    asset1_data = yf.download(asset1_ticker, start=start_date_year, end=end_date, interval='1d')
    asset2_data = yf.download(asset2_ticker, start=start_date_year, end=end_date, interval='1d')
    intraday_data_asset1 = yf.download(asset1_ticker, start=start_date_day, end=end_date, interval='1h')
    intraday_data_asset2 = yf.download(asset2_ticker, start=start_date_day, end=end_date, interval='1h')

    # Prepare data for analysis
    monthly_data = pd.concat([asset1_data['Close'], asset2_data['Close']], axis=1, keys=['Asset1', 'Asset2']).resample('M').mean()
    monthly_data['Asset1 Monthly Change'] = monthly_data['Asset1'].pct_change()
    monthly_data['Asset2 Monthly Change'] = monthly_data['Asset2'].pct_change()
    combined_data = pd.concat([asset1_data['Close'], asset2_data['Close']], axis=1, keys=['Asset1', 'Asset2'])
    combined_data['Asset1 Daily Change'] = combined_data['Asset1'].pct_change()
    combined_data['Asset1 7-day Change'] = combined_data['Asset1'].pct_change(periods=7)
    combined_data['Asset2 Daily Change'] = combined_data['Asset2'].pct_change()
    combined_data['Asset2 7-day Change'] = combined_data['Asset2'].pct_change(periods=7)

    # Correlation analysis
    monthly_correlation = monthly_data['Asset1 Monthly Change'].corr(monthly_data['Asset2 Monthly Change'])
    weekly_correlation = combined_data['Asset1 7-day Change'].corr(combined_data['Asset2 7-day Change'])
    daily_correlation = combined_data['Asset1 Daily Change'].corr(combined_data['Asset2 Daily Change'])

    # Calculate max and average divergence
    max_divergence_monthly, avg_divergence_monthly = max_and_avg_divergence(monthly_data['Asset1 Monthly Change'], monthly_data['Asset2 Monthly Change'])
    max_divergence_weekly, avg_divergence_weekly = max_and_avg_divergence(combined_data['Asset1 7-day Change'], combined_data['Asset2 7-day Change'])
    max_divergence_daily, avg_divergence_daily = max_and_avg_divergence(combined_data['Asset1 Daily Change'], combined_data['Asset2 Daily Change'])

    # Interpret and print the correlation results
    monthly_corr_value, monthly_corr_expl = interpret_correlation(monthly_correlation)
    weekly_corr_value, weekly_corr_expl = interpret_correlation(weekly_correlation)
    daily_corr_value, daily_corr_expl = interpret_correlation(daily_correlation)

    print("\nCorrelation Analysis Results:")
    print("----------------------------")
    print(f"{asset1_ticker} vs. {asset2_ticker}:")
    print(f"1. Daily Correlation:")
    print(f"   - Correlation Value: {daily_corr_value}")
    print(f"   - Interpretation: {daily_corr_expl}")
    print(f"2. 7-Day Correlation:")
    print(f"   - Correlation Value: {weekly_corr_value}")
    print(f"   - Interpretation: {weekly_corr_expl}")
    print(f"3. Monthly Correlation:")
    print(f"   - Correlation Value: {monthly_corr_value}")
    print(f"   - Interpretation: {monthly_corr_expl}")

    # Output the maximum and average divergence
    print("\nDivergence Analysis:")
    print("----------------------------")
    print(f"{asset1_ticker} vs. {asset2_ticker}:")
    print(f"1. Monthly Divergence:")
    print(f"   - Maximum Divergence: {max_divergence_monthly:.2%}")
    print(f"   - Average Divergence: {avg_divergence_monthly:.2%}")
    print(f"2. 7-Day Divergence:")
    print(f"   - Maximum Divergence: {max_divergence_weekly:.2%}")
    print(f"   - Average Divergence: {avg_divergence_weekly:.2%}")
    print(f"3. Daily Divergence:")
    print(f"   - Maximum Divergence: {max_divergence_daily:.2%}")
    print(f"   - Average Divergence: {avg_divergence_daily:.2%}")

    # Plotting the line graphs for visualization with precise percentage scales
    def plot_with_precise_percentage(data1, data2, title, xlabel, ylabel):
        plt.figure(figsize=(12, 6))
        plt.plot(data1.index, data1, label=asset1_ticker, color='blue')
        plt.plot(data2.index, data2, label=asset2_ticker, color='red')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(lambda y, _: '{:.2%}'.format(y)))
        plt.legend()
        plt.show()

    # Yearly Changes (by month)
    plot_with_precise_percentage(monthly_data['Asset1 Monthly Change'], monthly_data['Asset2 Monthly Change'], 'Monthly Percentage Change Over Last Year', 'Month', 'Percentage Change')

    # 7-Day Changes
    plot_with_precise_percentage(combined_data['Asset1 7-day Change'][-7:], combined_data['Asset2 7-day Change'][-7:], '7-Day Percentage Change', 'Date', 'Percentage Change')

    # Intraday Changes (last trading day)
    plot_with_precise_percentage(intraday_data_asset1['Close'].pct_change(), intraday_data_asset2['Close'].pct_change(), 'Intraday Hourly Percentage Change for Last Trading Day', 'Hour', 'Percentage Change')

# Run the analysis
analyze_assets_correlation()
