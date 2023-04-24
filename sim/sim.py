from data_scraping.twelve_data.twelve_data_scrape import get_tickers
from data_scraping.twelve_data.twelve_data_scrape import get_stock_data
from strategies.simple_ma import simulate_simple_ma


input_amount = print(input("Enter amount: "))

ticker = 'A'
stock_df = get_stock_data(ticker)
stock_df = simulate_simple_ma(input_amount, stock_df, 20, 50)