import matplotlib.pyplot as plt
import os


def plot_bollinger_bands(df, tkr):
    plt.figure(figsize=(20, 6))
    plt.plot(price_data_df[::-1])
    plt.legend(df.columns) 
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.xlim(df.index[0], df.index[-1])
    os.makedirs('out', exist_ok=True)
    plt.savefig(f'out/bolling_band_{tkr}')