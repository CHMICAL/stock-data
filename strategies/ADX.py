import pandas as pd
from data_scraping.twelve_data.twelve_data_scrape import get_csv_data
import numpy as np
import pprint as pprint
import matplotlib.pyplot as plt
from datetime import timedelta

def calc_true_range(price_data_df, day):
    v1 = price_data_df.loc[day, ['high']] - price_data_df.loc[day, ['low']]
    v2 = abs(price_data_df.loc[day, ['high']] - price_data_df.loc[day - timedelta(days=1), ['close']])
    v3 = abs(price_data_df.loc[day, ['low']] - price_data_df.loc[day - timedelta(days=1), ['close']])
    true_range = max(v1, v2, v3)
    return true_range   
    


def calculate_ADX(ticker, time_period=14):
    """
    Function to calculate ADX based on a given time period (default=14)
    to consider for smoothing the data.
    """
    data_df = get_csv_data(ticker)
    data_df.set_index(['datetime'], drop=True, inplace=True)
    data_df.index = pd.to_datetime(data_df.index)
    price_data_df = data_df.loc[:, ['close']]

    price_data_df[f'{time_period}_ADX'] = None
    price_data_df[f'True range'] = None

    for i, day in enumerate(price_data_df.index):
        current_TR = calc_true_range(price_data_df, day)
        average_TR = None
        for i2, day2 in enumerate(price_data_df.index):
            


            


        pdm = price_data_df.loc[day, ['high']] - price_data_df.loc[day - timedelta(days=1), ['high']]
        if pdm <= 0:
            pdm = 0
        ndm = price_data_df.loc[day, ['low']] - price_data_df.loc[day - timedelta(days=1), ['low']]
        dm = max(ndm, pdm)
        for 




