import pandas as pd
import ApiAuth
import requests
from bs4 import BeautifulSoup

#, stocks=None, stock_symbols=None

symbols = ['TSLA', 'TL0.DE', 'TSLA.MX', 'TL0.F']

#url = 'https://finance.yahoo.com/quote/{}'.format(name)

#resp = requests.get(url)
#soup = BeautifulSoup(resp.text, "html.parser")

df = ApiAuth.Stocks(stocks=None, stock_symbols=symbols).scrap()

print(df)