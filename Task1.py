import os
import sec_edgar_downloader
#Define the companies that I am going to track
#I'm going to be tracking Lazard, BNY Mellon, and JP Morgan
tickers = ['BK', 'LAZ', 'JPM']
start_year = 1995
end_year = 2023
new_dir = 'sec_files'

os.makedirs(new_dir, exist_ok=True)
downloader = sec_edgar_downloader.Downloader('Emily Sun', 'ilrhsun@gmail.com',)

for ticker in tickers:
    ticker_dir = os.path.join(new_dir, ticker)
    os.makedirs(ticker_dir, exist_ok=True)
    for year in range(start_year, end_year + 1):
        print(f"Downloading 10-k files for{ticker} in {year}... ")
        num_downloaded = downloader.get("10-K", ticker, after=f"{year}-01-01", before=f"{year+1}-01-01")
        print(f"Downloaded {num_downloaded} filings for {ticker} in {year}")
print("Download finished")

