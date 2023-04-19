import pandas as pd
from data_scraping.twelve_data.twelve_data_scrape import get_stock_data
from utilities.quantitive.basic_utils import build_sma_col
from utilities.quantitive.basic_utils import set_date_as_idx_and_dtobj
import numpy as np
import pprint as pprint
import matplotlib.pyplot as plt
from datetime import timedelta

def simulate_simple_ma(input_amount, stock_df, short_window, long_window):
    stock_df = set_date_as_idx_and_dtobj(stock_df)
    stock_df = build_sma_col(stock_df, short_window)
    stock_df = build_sma_col(stock_df, long_window)
    stock_df['returns'] = None
    
    cash = input_amount
    stock_holding = 0

    for i, cell in stock_df.iterrows():
        
        # Buy if short SMA goes above the long SMA
        if cell[f'{short_window}_SMA'] > cell[f'{long_window}_SMA'] and cash > 0:
            stock_price = cell['close']
            shares_to_buy = cash / stock_price
            stock_holding += shares_to_buy
            cash -= shares_to_buy * stock_price
        
        # Sell if short SMA goes below the long SMA
        elif cell[f'{short_window}_SMA'] < cell[f'{long_window}_SMA'] and stock_holding > 0:
            stock_price = cell['close']
            cash += stock_holding * stock_price
            stock_holding = 0
        
        # Calculate daily return
        if stock_holding > 0:
            stock_value = stock_holding * cell['close']
            total_value = cash + stock_value
            daily_return = (total_value - input_amount) / input_amount
            stock_df.at[i, 'returns'] = daily_return
        else:
            stock_df.at[i, 'returns'] = 0
            
    return stock_df


