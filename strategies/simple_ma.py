import pandas as pd

from data_scraping.twelve_data.twelve_data_scrape import get_csv_data
import numpy as np
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


def build_ma_strat_df(ticker):
	"""
	Builds basic 20 and 50 day ma df

	Parameters
	----------
	ticker: str, eg 'AMZN'

	Returns
	-------

	"""
	data_df = get_csv_data(ticker)

	data_df.set_index(['datetime'], drop=True, inplace=True)
	data_df.index = pd.to_datetime(data_df.index)

	price_data_df = data_df.loc[:, ['close']]

	price_data_df['20_SMA'] = None
	price_data_df['50_SMA'] = None

	for i, day in enumerate(price_data_df.index):
		price_data_df.loc[day, ['20_SMA']] = get_ma_from_df(days=20, df=price_data_df, i=i)

		price_data_df.loc[day, ['50_SMA']] = get_ma_from_df(days=50, df=price_data_df, i=i)

	price_data_df['holding'] = price_data_df['20_SMA'] > price_data_df['50_SMA']

	return price_data_df


def get_ma_from_df(days, df, i):
	return round(np.average(df['close'].values[i - days: i]), 2)


def build_returns_df(ticker, strat_df):
	strat_df = build_ma_strat_df(ticker)
	strat_df['action'] = None
	strat_df['return'] = None
	strat_df['tot_return'] = None
	strat_df.loc[strat_df.index[0], ['tot_return']] = 0

	for i, day in enumerate(strat_df.index[1:]):
		i += 1
		if not strat_df.loc[strat_df.index[i - 1], 'holding'] and\
			strat_df.loc[strat_df.index[i], 'holding']:
			strat_df.loc[day, ['action']] = 'BUY'

		if strat_df.loc[strat_df.index[i - 1], 'holding'] and\
			not strat_df.loc[strat_df.index[i], 'holding'] and\
			'BUY' in strat_df['action'].values[:i]:

			strat_df.loc[day, ['action']] = 'SELL'

			buy_price = strat_df[strat_df['action'] == 'BUY']['close'].values[-1]
			sell_price = strat_df.loc[day]['close']
			pct_return = (sell_price - buy_price) / buy_price

			strat_df.loc[day, ['return']] = pct_return

			last_tot_return = strat_df['tot_return'].dropna().values[-1]
			strat_df.loc[day, ['tot_return']] = ((1 + last_tot_return) * (1 + pct_return)) - 1

	return strat_df
