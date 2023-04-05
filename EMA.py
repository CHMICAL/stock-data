import requests
import pprint as pprint
import http.client
import pandas as pd
import json
import matplotlib.pyplot as plt

TICKER = 'AMZN'
DAYS = 300

with open(fr"tickers.txt", "r") as f:
    text = f.read()
    tickers = text.split("\n")

def main():
	# price_data_df = get_api_data(TICKER)
	data_df = get_csv_data(TICKER)
	data_df.set_index(keys='datetime', drop=True)

	price_data_df = data_df.loc[:, ['close']]

	price_data_df['20_SMA'] = None
	price_data_df['50_SMA'] = None

	for index, row in price_data_df.iterrows():
		if index - 20 >= 0:
			price_data_df.iloc[index]['20_SMA'] = (price_data_df.iloc[index - 20: index])/20

		if index - 50 >= 0:
			price_data_df.iloc[index]['50_SMA'] = (price_data_df.iloc[index - 50: index])/50

	plot = plt.plot(data=price_data_df)

	plot.savefig('out.csv')


def get_api_data(ticker):
	conn = http.client.HTTPSConnection("twelve-data1.p.rapidapi.com")

	headers = {
		'X-RapidAPI-Key': "1e0fd66d79msh05dad0e66812db1p1220abjsn66aa9d121d7c",
		'X-RapidAPI-Host': "twelve-data1.p.rapidapi.com"
		}

	conn.request("GET", f"/time_series?interval=1day&symbol={ticker}&format=json&outputsize={DAYS}", headers=headers)

	res = conn.getresponse()
	data = res.read()
	
	price_json = json.loads(data)

	price_data_df = pd.DataFrame(price_json['values'])

	price_data_df.csv(fr'Historical data/{ticker}.csv')

	return price_data_df

def get_csv_data(ticker):
	return pd.read_csv(fr'Historical data/{ticker}.csv')


main()

for ticker in tickers:
    get_api_data(ticker)