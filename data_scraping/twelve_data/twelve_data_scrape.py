import requests
import pprint as pprint
import http.client
import pandas as pd
import json
from os.path import exists
import time
import os
import pickle


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

def ticker_to_exchange_map(ticker, exchange_name):
    hashmap_val = {ticker : exchange_name}
    if exists(fr'{data_dir}/exchange_mapping.pickle'):
        with open(f'{data_dir}/exchange_mapping.pickle', 'rb') as f:
            hashmap = pickle.load(f)
            hashmap[ticker] = exchange_name
        with open(f'{data_dir}/exchange_mapping.pickle', 'wb') as f:
            pickle.dump(hashmap, f)
    else:
        with open(f'{data_dir}/exchange_mapping.pickle', 'wb') as f:
            pickle.dump(hashmap_val, f)

def exchange_name_check(ticker):
    with open(f'{data_dir}/exchange_mapping.pickle', 'rb') as f:
        hashmap = pickle.load(f)
        exchange_name = hashmap[ticker] 
    return exchange_name

def get_api_data(ticker, days):
    if exists(fr'{data_dir}/{ticker}.csv') and exists(fr'{data_dir}/{ticker}.json'):
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
        meta_data_json = price_json['meta']
        exchange_name = meta_data_json['exchange']
        ticker_to_exchange_map(ticker, exchange_name)
        subfolder = os.path.join(data_dir, exchange_name)
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        with open(os.path.join(subfolder, f"{ticker}.json"), "w") as outfile:
            json.dump(meta_data_json, outfile)
        price_data_df.to_csv(os.path.join(subfolder, f"{ticker}.csv"))

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

def get_stock_data(ticker):
    exchange_name = exchange_name_check(ticker)
    df = pd.read_csv(f'{data_dir}/{exchange_name}/{ticker}.csv', index_col=[0])
    df.set_index(['datetime'], drop=True, inplace=True)
    df.index = pd.to_datetime(df.index)
    return df


data_dir = "data_scraping/twelve_data/data"
years_to_scrape = 13
tickers = get_tickers()

for ticker in tickers:
    get_api_data(ticker, days = 365*years_to_scrape)
    break
    

