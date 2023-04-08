from data_scraping.twelve_data_scrape import get_api_data, get_csv_data


def build_ma_df(get_latest_data=False):
	"""
	Builds basic 20 and 50 day ma df

	Parameters
	----------
	get_latest_data: bool

	Returns
	-------

	"""
	if get_latest_data:
		data_df = get_api_data('AMZN')
	else:
		data_df = get_csv_data('AMZN')
	data_df.set_index(keys='datetime', drop=True)

	price_data_df = data_df.loc[:, ['close']]

	price_data_df['20_SMA'] = None
	price_data_df['50_SMA'] = None

	for index, row in price_data_df.iterrows():
		if index - 20 >= 0:
			price_data_df.iloc[index]['20_SMA'] = (price_data_df.iloc[index - 20: index])/20

		if index - 50 >= 0:
			price_data_df.iloc[index]['50_SMA'] = (price_data_df.iloc[index - 50: index])/50

	return price_data_df
