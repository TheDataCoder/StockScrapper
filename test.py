import ApiAuth
import requests
from bs4 import BeautifulSoup


symbols = ['advadv', 'TL0.DE', 'TSLA.MX', 'TL0.F']

df = ApiAuth.Stocks().scrap(stock_symbols=symbols)
print(df)

for symbol in df['Symbol'].values:
    url = 'https://finance.yahoo.com/quote/{}'.format(symbol)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

