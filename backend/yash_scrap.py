from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os

# Base URL for Finviz stock news
finviz_url = 'https://finviz.com/quote.ashx?t='
tickers = ['AMZN', 'GOOG', 'DRUG', 'AAPL']
output_directory = "news"

# Create a directory to store text files if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

news_tables = {}
for ticker in tickers:
    url = finviz_url + ticker

    # Request the page with custom headers to avoid being blocked
    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)

    # Parse the HTML content
    html = BeautifulSoup(response, features='html.parser')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table

# Parse the news table data and save it to text files
for ticker, news_table in news_tables.items():
    # Open a text file to save the scraped data for each ticker
    with open(f"{output_directory}/{ticker}_news.txt", 'w') as file:
        for row in news_table.findAll('tr'):
            title = row.a.text
            date_data = row.td.text.split(' ')

            if len(date_data) == 1:
                time = date_data[0]
                date = None  # No date, just time (for recent news)
            else:
                date = date_data[0]
                time = date_data[1]

            # Write the news headline, date, and time to the text file
            file.write(f"Date: {date}, Time: {time}, Headline: {title}\n")

print(f"News data scraped and saved to '{output_directory}' folder.")