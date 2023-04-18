import requests
import pprint as pprint
import http.client
import pandas as pd
import json
from os.path import exists
import time


def get_tickers():
    with open(fr"data_scraping\twelve_data\tickers.txt", "r") as f:
        text = f.read()
        tickers = text.split("\n")
        tickers = [ticker.strip() for ticker in tickers]
    return tickers

   
'''
Scrapes data for all tickers in tickers.txt (around 7900 tickers)

args:
    ticker (str), number of days (int)

output:
    csv files in data_scraping/twelve_data for each ticker
'''

def get_api_data(ticker, days):
    #To stop per minute API call limit from being reached... 
    if exists(fr'{csv_dir}/{ticker}.csv'):
            return
    tickers_with_err_msg = []
    conn = http.client.HTTPSConnection("twelve-data1.p.rapidapi.com")

    headers = {
    "X-RapidAPI-Key": "0d349eee06msh138e9a789c8ef8dp14c0f3jsnd4506bccc0b4",
    "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
    }

    conn.request("GET", f"/time_series?interval=1day&symbol={ticker}&format=json&outputsize={days}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    price_json = json.loads(data)
    try:
        price_data_df = pd.DataFrame(price_json['values'])
        meta_data_df = pd.DataFrame(price_json['meta'])
        price_data_df = price_data_df.concat(meta_data_df)
        price_data_df.to_csv(fr'data_scraping/twelve_data/csvs/{ticker}.csv')
    except KeyError:
        error_string = f"{ticker}: {price_json['message']}"
        print(error_string)
        if 'You have exceeded' in price_json['message']:
            print("Limit reached...waiting 1 minute...")
            time.sleep(60)
            print("Starting again...")
            get_api_data(ticker, days)
        else:
            tickers_with_err_msg.append(error_string)

def get_csv_data(ticker):
    df = pd.read_csv(f'data_scraping/twelve_data/csvs/{ticker}.csv', index_col=[0])
    df.set_index(['datetime'], drop=True, inplace=True)
    df.index = pd.to_datetime(df.index)
    return df


csv_dir = "data_scraping/twelve_data/csvs"
years_to_scrape = 13
tickers = get_tickers()

for ticker in tickers:
    get_api_data(ticker, days = 365*years_to_scrape)
    break
    

