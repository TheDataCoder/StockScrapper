import GStocks
import requests
import pandas as pd
from bs4 import BeautifulSoup

symbols = ['advadv', 'TL0.DE', 'TSLA.MX', 'TL0.F']

df = GStocks.scrap(stock_symbols=symbols)

def fill_table(dataframe):

    columns = ['Previous Close', 'Open', "Day's Range", '52 Week Range', 'Beta', 'PE Ratio', 'EPS', 'Earnings Date', 'Ex-Dividend Date']

    cells = ['PREV_CLOSE-value', 'OPEN-value', 'DAYS_RANGE-value', 'FIFTY_TWO_WK_RANGE-value', 'BETA_5Y-value',
             'PE_RATIO-value', 'EPS_RATIO-value', 'EARNINGS_DATE-value', 'EX_DIVIDEND_DATE-value']

    values, L = [], []

    for symbol in dataframe['Symbol'].values:
        url = 'https://finance.yahoo.com/quote/{}'.format(symbol)
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")

        for cell in cells:
            values.append(soup.find_all('div', {'id': 'quote-summary'})[0].find('td', {'data-test': cell}).text)
        L.append(values)
        values = []

    return pd.concat([dataframe, pd.DataFrame(L, columns=columns)], axis=1)

dataframe = fill_table(df)
print(dataframe.head())