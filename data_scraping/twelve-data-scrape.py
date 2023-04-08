import http.client
import pandas as pd
import json

TICKER = 'AMZN'
DAYS = 300

with open(fr"../tickers.txt", "r") as f:
    text = f.read()
    tickers = text.split("\n")


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

	price_data_df.to_csv(fr'twelve_data/{ticker}.csv')

	return price_data_df

def get_csv_data(ticker):
	return pd.read_csv(fr'twelve_data/{ticker}.csv')


for ticker in tickers:
    get_api_data(ticker)