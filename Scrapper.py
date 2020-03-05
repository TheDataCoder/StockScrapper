from bs4 import BeautifulSoup
import requests
import sys
from datetime import datetime, timedelta
import pandas as pd

def names(stocks):
    data = pd.DataFrame()
    for name in stocks:
        url = "https://finance.yahoo.com/lookup?s={}".format(name)
        d = pd.read_html(url)
        df = d[0].dropna(axis=0, thresh=4)
        df = df.drop('Industry / Category', 1)
        df = df[df['Name'].str.contains(name, case=False)]
        data = pd.concat([data, df], ignore_index=True)
    return data

def symbols(stock_symbols):
    data = pd.DataFrame()
    for symbol in stocks:
        url = "https://finance.yahoo.com/lookup?s={}".format(symbol)
        d = pd.read_html(url)
        df = d[0].dropna(axis=0, thresh=4)
        df = df.drop('Industry / Category', 1)
        df = df[df['Symbol'].str.contains(symbol, case=False)]
        data = pd.concat([data, df], ignore_index=True)
    return data

names(['Tesla', 'Keyence'])