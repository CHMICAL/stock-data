import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def simple_datetime_price_plot(df, tkr):
    plt.figure(figsize=(20, 6))
    plt.plot(df[::-1])

    plt.legend(df.columns)

    plt.xlabel('Date')
    plt.ylabel('Price ($)')

    plt.xlim(df.index[0], df.index[-1])

    plt.savefig(f'out/simple_ma_{tkr}')