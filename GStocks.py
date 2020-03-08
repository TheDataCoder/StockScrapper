from __future__ import print_function
import os

import requests
from bs4 import BeautifulSoup
import pandas as pd

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from time import localtime, strftime
from requests.utils import requote_uri


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class ApiAuth:

    def __init__(self, scopes, client_secret_file, application_name):
        self.scopes = scopes
        self.client_secret_file = client_secret_file
        self.application_name = application_name

    def getCredentials(self):

        """Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        :return:
            Credentials, the obtained credential.
        """

        current_dir = os.getcwd()
        credentials_dir = os.path.join(current_dir, '.credentials')

        if not os.path.exists(credentials_dir):
            os.makedirs(credentials_dir)
        credential_path = os.path.join(credentials_dir, 'google-drive-credentials.json')
        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.client_secret_file, self.scopes)
            flow.user_agent = self.application_name
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)

        return credentials


def scrap(stocks=None, stock_symbols=None):
    """
    Scrap the stock prices by inputting stock names or stock symbols and save them pd DataFrame.

    Parameters
    ----------
    stocks : list
            List of stocks

    stock_symbols : list
            List of stock symbols (Reuters Instrument Code)

    Returns
    ----------
    stock_frame : df
            Pandas DataFrame with scrapped stock prices
    """

    def names(stock_names):
        data = pd.DataFrame()
        for name in stock_names:
            url = "https://finance.yahoo.com/lookup?s={}".format(name)
            url = requote_uri(url)
            resp = requests.get(url).text
            soup = BeautifulSoup(resp, "lxml")
            not_found = soup.find_all('div', {'Mt(25px) Bdw(1px) Bdc($borderGray) Bds(s) Bdrs(3px) Pt(50px) Pb(60px) Px(15px) smartphone_Mx(20px) smartphone_Mb(30px)'})
            if not_found:
                print('stock ' + name + ' was not found')
            else:
                d = pd.read_html(url)
                df = d[0].dropna(axis=0, thresh=4)
                df = df.drop('Industry / Category', 1)
                df = df[df['Name'].str.contains(name, case=False)]
                data = pd.concat([data, df], ignore_index=True)
        return data

    def symbols(stock_symbols_):
        data = pd.DataFrame()
        for symbol in stock_symbols_:
            url = "https://finance.yahoo.com/lookup?s={}".format(symbol)
            url = requote_uri(url)
            resp = requests.get(url).text
            soup = BeautifulSoup(resp, "lxml")
            not_found = soup.find_all('div', {'Mt(25px) Bdw(1px) Bdc($borderGray) Bds(s) Bdrs(3px) Pt(50px) Pb(60px) Px(15px) smartphone_Mx(20px) smartphone_Mb(30px)'})
            if not_found:
                print('stock ' + symbol + ' was not found')
            else:
                d = pd.read_html(url)
                df = d[0].dropna(axis=0, thresh=4)
                df = df.drop('Industry / Category', 1)
                df = df[df['Symbol'].str.contains(symbol, case=False)]
                data = pd.concat([data, df], ignore_index=True)
        return data

    def fill_table(dataframe):

        columns = ['Previous Close', 'Open', "Day's Range", '52 Week Range', 'Beta', 'PE Ratio', 'EPS',
                   'Earnings Date', 'Ex-Dividend Date']

        cells = ['PREV_CLOSE-value', 'OPEN-value', 'DAYS_RANGE-value', 'FIFTY_TWO_WK_RANGE-value', 'BETA_5Y-value',
                 'PE_RATIO-value', 'EPS_RATIO-value', 'EARNINGS_DATE-value', 'EX_DIVIDEND_DATE-value']

        values, L = [], []

        for symbol in dataframe['Symbol'].values:
            url = 'https://finance.yahoo.com/quote/{}'.format(symbol)
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")

            for cell in cells:
                try:
                    values.append(soup.find_all('div', {'id': 'quote-summary'})[0].find('td', {'data-test': cell}).text)
                except AttributeError:
                    values.append('N/A')
            L.append(values)
            values = []

        return pd.concat([dataframe, pd.DataFrame(L, columns=columns)], axis=1)

    if stocks is not None:
        stock_frame = names(stocks)
    if stock_symbols is not None:
        stock_frame = symbols(stock_symbols)

    print('DataFrame built')
    return fill_table(stock_frame)


def write_cloud(stock_frame, service_drive, service_spread):
    """
    Upload the scrapped data to google docks spreadsheet.

    Parameters
    ----------
    stock_frame : Pandas DataFrame
            DataFrame with stock tickers and prices

    service_drive
            Google API discovery drive client

    service_spread
            Google API discovery sheets client

    """

    def check_dupe(services_drive, services_spread):
        files = services_drive.files().list().execute().get('files', [])
        for dict in files:
            if dict['name'] == 'Stocks':
                print('Sheet checked')
                return dict['id']
        spreadsheet = {'properties': {
            'title': 'Stocks'
        }
        }
        request = services_spread.spreadsheets().create(body=spreadsheet, fields='spreadsheetId')
        response = request.execute()
        print('Sheet created')
        return response['spreadsheetId']

    spreadsheetID = check_dupe(service_drive, service_spread)

    st = strftime("%Y.%m.%d_%H-%M-%S", localtime())

    new_request = {
          "requests": [
            {
              "addSheet": {
                "properties": {
                  "title": st}
              }
            }]}

    new_response = service_spread.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=new_request)
    new_response.execute()

    write_range = st + '!B2'

    response_date = service_spread.spreadsheets().values().append(
        spreadsheetId=spreadsheetID,
        valueInputOption='RAW',
        range=write_range,
        body=dict(
            majorDimension='ROWS',
            values=stock_frame.T.reset_index().T.values.tolist()
        )
    )

    response_date.execute()


def set_limit(stock_limit, stock_frame):
    """
    Change colors according to price fluctuations

    Parameters
    ----------
    stock_limit : list of tuples
            List of the uppest and lowest prices

    stock_frame : Pandas DataFrame
            DataFrame with stock tickers and prices

    Returns
    ----------
    stock_frame : df
        Pandas DataFrame modified according to set alerts

    """
    pass