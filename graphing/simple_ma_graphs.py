from strategies.simple_ma import build_ma_df
import matplotlib.pyplot as plt

def plots():
    price_data_df = build_ma_df()
    plot = plt.plot(data=price_data_df)

    plot.savefig('out.csv')