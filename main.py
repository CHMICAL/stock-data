from graphing.simple_ma_graphs import plot_strat_df
from strategies.simple_ma import build_ma_strat_df, build_returns_df


def main():
    """
    Main func to faff in
    """
    tkr = 'AMZN'
    strat_df = build_ma_strat_df(tkr)
    plot_strat_df(strat_df, tkr)
    returns_df = build_returns_df(tkr, strat_df)
    returns_df.to_csv(f'out/{tkr}_strat_details.csv')


if __name__ == '__main__':
    main()
