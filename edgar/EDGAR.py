from sec_edgar_downloader import Downloader
from bs4 import BeautifulSoup


dl = Downloader(fr"F:\Coding\Trading\BOT")

dl.get("10-K", "TSLA")

# with open(fr"F:\Coding\Trading\BOT\Filings\8-K\sec-edgar-filings\TSLA\8-K\0001564590-20-022062\full-submission.txt", "rb") as f:
#     filing = f.read()

# soup = BeautifulSoup(filing, "lxml")

# text = soup.get_text()

# print(text)