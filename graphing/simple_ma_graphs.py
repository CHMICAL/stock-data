import matplotlib.pyplot as plt
import os


def plot_strat_df(df, tkr):
    df.drop('holding', axis=1, inplace=True)
    plt.figure(figsize=(20, 6))
    plt.plot(df)

    plt.legend(df.columns)

    plt.xlabel('Date')
    plt.ylabel('Price ($)')

    plt.xlim(df.index[0], df.index[-1])

    os.makedirs('out', exist_ok=True)
    plt.savefig(f'out/simple_ma_{tkr}')