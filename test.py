import ApiAuth
import requests
import pandas as pd
from bs4 import BeautifulSoup



symbols = ['advadv', 'TL0.DE', 'TSLA.MX', 'TL0.F']

df = ApiAuth.Stocks().scrap(stock_symbols=symbols)

def fill_table(dataframe):

    columns = ['Previous Close', 'Open', "Day's Range", '52 Week Range', 'Beta', 'PE Ratio', 'EPS', 'Earnings Date', 'Ex-Dividend Date']

    prev_close, current_open, day_range, weeks_range, beta, PERatio, EPS, EarningsDATE, ExDividendDATE = [], [], [], [], [], [], [], [], []

    for symbol in dataframe['Symbol'].values:
        url = 'https://finance.yahoo.com/quote/{}'.format(symbol)
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")

        prev_close.append(soup.find_all('div', {'id': 'quote-summary'})[0].find('td', {'data-test': 'PREV_CLOSE-value'}).text)
        current_open.append(soup.find_all('div', {'id': 'quote-summary'})[0].find('td', {'data-test': 'OPEN-value'}).text)
        day_range.append(soup.find_all('div', {'id': 'quote-summary'})[0].find('td', {'data-test': 'DAYS_RANGE-value'}).text)
        weeks_range.append(soup.find_all('div', {'id': 'quote-summary'})[0].find('td',
                                                                            {'data-test': 'FIFTY_TWO_WK_RANGE-value'}).text)
        beta.append(soup.find_all('div', {'id': 'quote-summary'})[0].find('td', {'data-test': 'BETA_5Y-value'}).text)
        PERatio.append(soup.find_all('div', {'id': 'quote-summary'})[0].find('td', {'data-test': 'PE_RATIO-value'}).text)
        EPS.append(soup.find_all('div', {'id': 'quote-summary'})[0].find('td', {'data-test': 'EPS_RATIO-value'}).text)
        EarningsDATE.append(soup.find_all('div', {'id': 'quote-summary'})[0].find('td',
                                                                             {'data-test': 'EARNINGS_DATE-value'}).text)
        ExDividendDATE.append(soup.find_all('div', {'id': 'quote-summary'})[0].find('td',
                                                                               {'data-test': 'EX_DIVIDEND_DATE-value'}).text)

    dataframe[columns] = prev_close, current_open, day_range, weeks_range, beta, PERatio, EPS, EarningsDATE, ExDividendDATE

    return df


fill_table(df)
print(df.head())