import pandas as pd
# from data_scraping.twelve_data.twelve_data_scrape import get_csv_data
import numpy as np
import pprint as pprint
import matplotlib.pyplot as plt
 



def bollinger_bands(ticker, time_period):

    data_df = get_csv_data(ticker)
    data_df.set_index(['datetime'], drop=True, inplace=True)
    data_df.index = pd.to_datetime(data_df.index)
    price_data_df = data_df.loc[:, ['close']]

    price_data_df[f'{time_period}_SMA'] = None

    for i, day in enumerate(price_data_df.index):
        price_data_df.loc[day, [f'{time_period}_SMA']] = round(np.average(price_data_df['close'][i : i + {time_period}]), 2)

    price_data_df['bolling_up'] = None
    price_data_df['bolling_low'] = None
    # bolling_up = SMA+(2*n Standard Deviation of Close).
    # bolling_down = SMA-(2*n Standard Deviation of Close).

    for i, day in enumerate(price_data_df.index):
        total = 0
        if i == (len(price_data_df['close'] - (time_period - 1))):
            break
        else:
            for i2, day2 in enumerate(price_data_df.index):
                if i2 in range(i, i + time_period):
                    dist_to_mean_sq = (price_data_df['close'][i2] - price_data_df[f'{time_period}_SMA'][i])**2
                    total += dist_to_mean_sq
                
        stand_deviation = np.sqrt(total / (time_period - 1))

        price_data_df.loc[day, ['bolling_up']] = price_data_df[f'{time_period}_SMA'][i] + (stand_deviation * 2)
        price_data_df.loc[day, ['bolling_low']] = price_data_df[f'{time_period}_SMA'][i] - (stand_deviation * 2)
    
    price_data_df = price_data_df[::-1]
    return price_data_df
    



time_period = 20

for ticker in tickers:
    bollinger_bands(ticker, time_period)    

