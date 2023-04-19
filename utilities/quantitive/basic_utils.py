import pandas as pd
import numpy as np

'''
Functions to build basic technical indicators.

Parameters:
    df (pandas.DataFrame): A dataframe containing stock data for a specific stock.

Returns:
    df (pandas.DataFrame): Additional column(s) with values for the technical indicator
'''

def build_sma_col(df, window_size):
    df[f'{window_size}_SMA'] = df['close'].rolling(window_size).mean().round(2)
    return df

def build_ema_col(df, window_size):
    df[f'{window_size}_EMA'] = df['close'].ewm(span=window_size, adjust=False).mean()
    return df

def build_bollinger_cols(df, window_size):
    df['bolling_up'] = None
    df['bolling_down'] = None

    for i, day in enumerate(df.index):
        if i < window_size - 1:
            continue
        window = df.iloc[i - window_size + 1: i + 1]
        mean = window['close'].mean()
        std = window['close'].std()
        df.loc[day, 'bolling_up'] = mean + 2 * std
        df.loc[day, 'bolling_down'] = mean - 2 * std

    return df

def build_rsi_col(df, window_size):
    delta = df['close'].diff()
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    avg_gain = gains.rolling(window_size).mean()
    avg_loss = losses.rolling(window_size).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    df['RSI'] = rsi
    return df

def build_stochastics(df, window_size):
    low_min = df['low'].rolling(window_size).min()
    high_max = df['high'].rolling(window_size).max()

    df['%K'] = 100 * ((df['close'] - low_min) / (high_max - low_min))
    df['%D'] = df['%K'].rolling(window=3).mean()

    return df

def build_macd_col(df, fast_window=12, slow_window=26, signal_window=9):
    ema_fast = df['close'].ewm(span=fast_window, min_periods=fast_window, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow_window, min_periods=slow_window, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal = macd.ewm(span=signal_window, min_periods=signal_window, adjust=False).mean()
    histogram = macd - signal
    df['MACD'] = macd
    df['MACD_signal'] = signal
    df['MACD_hist'] = histogram
    return df

def build_atr_col(df, window_size=14):
    tr1 = abs(df['high'] - df['low'])
    tr2 = abs(df['high'] - df['close'].shift())
    tr3 = abs(df['low'] - df['close'].shift())
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = true_range.rolling(window_size).mean()
    df['ATR'] = atr
    return df

def build_obv_col(df):
    obv = np.where(df['close'] > df['close'].shift(1), df['volume'], np.where(df['close'] < df['close'].shift(1), -df['volume'], 0)).cumsum()
    df['OBV'] = obv
    return df

def build_roc_col(df, window_size=14):
    roc = ((df['close'] - df['close'].shift(window_size)) / df['close'].shift(window_size)) * 100
    df['ROC'] = roc
    return df

def build_fibonacci_col(df, high_col='high', low_col='low'):
    high = df[high_col]
    low = df[low_col]
    diff = high - low
    levels = [0.236, 0.382, 0.5, 0.618, 0.786]
    for level in levels:
        df[f'Fib{level}'] = high - (diff * level)
    return df

def build_adx_col(df, window_size):
    tr1 = abs(df['high'] - df['low'])
    tr2 = abs(df['high'] - df['close'].shift())
    tr3 = abs(df['low'] - df['close'].shift())
    true_range = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)
    dm_plus = np.where((df['high'] - df['high'].shift()) > (df['low'].shift() - df['low']), 
                       (df['high'] - df['high'].shift()), 0)
    dm_minus = np.where((df['low'].shift() - df['low']) > (df['high'] - df['high'].shift()), 
                        (df['low'].shift() - df['low']), 0)
    smooth_tr = true_range.rolling(window_size).mean()
    smooth_dm_plus = dm_plus.rolling(window_size).mean()
    smooth_dm_minus = dm_minus.rolling(window_size).mean()
    di_plus = 100 * smooth_dm_plus / smooth_tr
    di_minus = 100 * smooth_dm_minus / smooth_tr
    dx = 100 * abs(di_plus - di_minus) / (di_plus + di_minus)
    adx = dx.rolling(window_size).mean()
    adx_col = pd.Series(adx, name='ADX')
    df = df.join(adx_col)
    return df

def build_envelopes_col(df, window_size, envelope_size):
    ma = df['close'].rolling(window_size).mean()
    upper_band = ma * (1 + envelope_size/100)
    lower_band = ma * (1 - envelope_size/100)
    envelopes_col = pd.DataFrame({'Upper Band': upper_band, 'Lower Band': lower_band})
    df = df.join(envelopes_col)
    return df

def build_williamsr_col(df, window_size):
    highest_high = df['high'].rolling(window_size).max()
    lowest_low = df['low'].rolling(window_size).min()
    williams_r = -100 * (highest_high - df['close']) / (highest_high - lowest_low)
    williamsr_col = pd.Series(williams_r, name='Williams %R')
    df = df.join(williamsr_col)
    return df



'''
set_date_as_idx_and_dtobj

Parameters:
    df (pandas.DataFrame): A dataframe containing stock data for a specific stock.

Returns:
    df (pandas.DataFrame): Sets the date as the index of the df. Converts the index to datetime objects
'''
def set_date_as_idx_and_dtobj(df):
    df.set_index(['datetime'], drop=True, inplace=True)
    df.index = pd.to_datetime(df.index)
    return df