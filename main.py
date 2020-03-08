"""
A small script to get data from yahoo finance and upload it to your Google Spreadsheet

Further development may include direct export to csv file and setting alarms to user in case if stock price drops
"""


from __future__ import print_function
import httplib2
import csv
import numpy as np

from apiclient import discovery

import GStocks

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file']

# Get json file form https://console.cloud.google.com

CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Stocks'

authInst = GStocks.ApiAuth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)
spreadsheet_service = discovery.build('sheets', 'v4', http=http)

def csv_reader():

    while True:
        path = str(input())
        if path[-4:] == '.csv':
            try:
                csv_file = open(path)
                csv_read = csv.reader(csv_file)
                stocks_csv = [item for sublist in list(csv_read) for item in sublist]
                return stocks_csv
            except OSError:
                print('You have entered the unexisting path')
                print('Please provide a path to the CSV files with stock names: ')
                continue
        else:
            print('The file path did not lead to csv file')
            print('Please re-enter the path or enter: ')
            continue

while True:
    print('Please specify if you want to enter stock names or stock symbols')
    print('Enter 1 for stock names, 2 for stock symbols, 3 to quit: ')
    f = input()
    if f == '1':
        print('Would you like to enter stock names manually or use CSV file?')
        print('Enter 1 to enter stock names manually, 2 to load from file: ')
        f = input()
        if f == '1':
            print('Please enter the stock names separated by space')
            stocks = [i for i in input().split(',')]
        elif f == '2':
            print('Please enter the path to your csv file including file name i.e. stocks.csv:')
            stocks = csv_reader()
        else:
            print('Please choose from 1 or 2')
            continue
        stocks_frame = GStocks.scrap(stocks)
        stocks_frame.replace(np.nan, '', inplace=True)
        GStocks.write_cloud(stocks_frame, drive_service, spreadsheet_service)
        break
    elif f == '2':
        print('Would you like to enter stock names manually or use CSV file?')
        print('Enter 1 to enter stock names manually, 2 to load from file: ')
        f = input()
        if f == '1':
            print('Please enter the stock symbols separated by space')
            stock_symbols = [i for i in input().split(',')]
        elif f == '2':
            print('Please enter the path to your csv file including file name i.e. stocks.csv:')
            stock_symbols = csv_reader()
        else:
            print('Please choose from 1 or 2')
            continue
        stocks_frame = GStocks.scrap(stock_symbols)
        stocks_frame.replace(np.nan, '', inplace=True)
        GStocks.write_cloud(stocks_frame, drive_service, spreadsheet_service)
        break
    elif f == '3':
        break
    else:
        print('You have entered wrong key')
        continue
