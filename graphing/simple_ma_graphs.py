from strategies.simple_ma import build_ma_df
import matplotlib.pyplot as plt

def simple_datetime_price_plot(df, tkr):
    plt.figure(figsize=(20, 6))
    plt.plot(df[::-1])

    plt.legend(df.columns)

    plt.xlabel('Date')
    plt.ylabel('Price ($)')

    plt.savefig(f'out/simple_ma_{tkr}')