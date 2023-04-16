import pandas as pd
from data_scraping.twelve_data.twelve_data_scrape import get_csv_data
import numpy as np
import pprint as pprint
import matplotlib.pyplot as plt

with open(fr"data_scraping\twelve_data\tickers.txt", "r") as f:
    text = f.read()
    tickers = text.split("\n")
    tickers = [ticker.strip() for ticker in tickers]


def build_stochastics(ticker, time_period):
    """
    Calculate the Stochastic Oscillator for a given DataFrame and period time_period.
    """
    data_df = get_csv_data(ticker)
    data_df.set_index(['datetime'], drop=True, inplace=True)
    data_df.index = pd.to_datetime(data_df.index)

    # Calculate the rolling minimum and maximum for the time period
    low_min = data_df['low'].rolling(window=time_period).min()
    high_max = data_df['high'].rolling(window=time_period).max()

    # Calculate the %K and %D values
    data_df['%K'] = 100 * ((data_df['close'] - low_min) / (high_max - low_min))
    data_df['%D'] = data_df['%K'].rolling(window=3).mean()

    return data_df

time_period = 20

print(build_stochastics("AMZN", time_period))