from graphing.simple_ma_graphs import simple_datetime_price_plot
from strategies.simple_ma import build_ma_df


def main():
    """
    Main func to faff in
    """
    tkr = 'AMZN'
    df = build_ma_df(tkr)
    simple_datetime_price_plot(df, tkr)


if __name__ == '__main__':
    main()