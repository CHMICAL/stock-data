import pandas as pd
# from data_scraping.twelve_data.twelve_data_scrape import get_csv_data
import numpy as np
import pprint as pprint
import matplotlib.pyplot as plt
from tabulate import tabulate




with open(fr"data_scraping\twelve_data\tickers.txt", "r") as f:
    text = f.read()
    tickers = text.split("\n")
    tickers = [ticker.strip() for ticker in tickers]

def build_rsi_df(ticker, time_period):
    '''
    Calculate the relative strength: mean of all the gains in the last n days / mean of all the losses  in the last n days
    Calculate the RSI: RSI = 100 - (100 / (1+RS))
    '''
    data_df = get_csv_data(ticker)
    data_df.set_index(['datetime'], drop=True, inplace=True)
    data_df.index = pd.to_datetime(data_df.index)
    price_data_df = data_df.loc[:, ['close']]

    price_data_df['gain'] = None
    price_data_df['loss'] = None
    price_data_df['change'] = None

    for i, day in enumerate(price_data_df.index):
        if i == (len(price_data_df['close'] - (time_period - 1))):
            break
        else:
            prev_price = price_data_df['close'][i + 1]
            current_price = price_data_df['close'][i]
            change = current_price - prev_price
            price_data_df.loc[day, ['change']] = change
            if current_price <= prev_price:
                loss = prev_price - current_price
                price_data_df.loc[day, ['gain']] = float(0)
                price_data_df.loc[day, ['loss']] = loss
            if current_price >= prev_price:
                gain = current_price - prev_price
                price_data_df.loc[day, ['gain']] = gain
                price_data_df.loc[day, ['loss']] = float(0)

    price_data_df['avg gain'] = None
    price_data_df['avg loss'] = None
    price_data_df['RS'] = None
    price_data_df['RSI'] = None

    for i, day in enumerate(price_data_df.index):
        if i == len(price_data_df['close']) - time_period:
            break
        else:
            # avg gain and avg loss...
            avg_gain = np.average(price_data_df['gain'][i : i + time_period - 1])
            avg_loss = np.average(price_data_df['loss'][i : i + time_period - 1])
            price_data_df.loc[day, ['avg gain']] = avg_gain
            price_data_df.loc[day, ['avg loss']] = avg_loss
        

            # RS and RSI...
            relative_strength = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + relative_strength))
            price_data_df.loc[day, ['RS']] = relative_strength
            price_data_df.loc[day, ['RSI']] = rsi





time_period = 14

# for ticker in tickers:
#     build_rsi_df(ticker, time_period)


    ###### Not sure this is producing correct results... I need to fix and test it...
                    
