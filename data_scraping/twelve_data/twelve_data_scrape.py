import http.client
import logging

import pandas as pd
import json


def get_api_data(ticker, days):
	conn = http.client.HTTPSConnection("twelve-data1.p.rapidapi.com")

	headers = {
		'X-RapidAPI-Key': "1e0fd66d79msh05dad0e66812db1p1220abjsn66aa9d121d7c",
		'X-RapidAPI-Host': "twelve-data1.p.rapidapi.com"
		}

	conn.request("GET", f"/time_series?interval=1day&symbol={ticker}&format=json&outputsize={days}", headers=headers)

	res = conn.getresponse()

	if res.status is not 200:
		raise ConnectionError(res.msg)
	
	price_json = json.loads(res.read())

	price_data_df = pd.DataFrame(price_json['values'])

	price_data_df.to_csv(fr'twelve_data/{ticker}.csv')


def get_csv_data(ticker):
	return pd.read_csv(f'data_scraping/twelve_data/csvs/{ticker}.csv', index_col=[0])


def scrape_all_tickers(years_to_scrape=5):
	"""
	Scrapes all data for all tickers in tickers.txt

	Parameters
	----------
	years_to_scrape: int, defaults to 5, number of years to scrape back
	"""
	with open(fr"tickers.txt", "r") as f:
		text = f.read()
		tickers = text.split("\n")

	for ticker in tickers:
		try:
			get_api_data(ticker, days=365*years_to_scrape)

		except ConnectionError:
			logging.warning(f'API rejected data request for {ticker}. Continuing')
			continue
