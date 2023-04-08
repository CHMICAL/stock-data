import pandas as pd

from data_scraping.twelve_data.twelve_data_scrape import get_csv_data
import numpy as np


def build_ma_df(ticker):
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
		price_data_df.loc[day, ['20_SMA']] = round(np.average(price_data_df['close'][i : i + 19]), 2)

		price_data_df.loc[day, ['50_SMA']] = round(np.average(price_data_df['close'][i : i + 49]), 2)

	return price_data_df
