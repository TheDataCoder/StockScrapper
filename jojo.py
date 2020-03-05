from __future__ import print_function
import httplib2
import os
import csv

from apiclient import discovery
from oauth2client import tools, file, client
from oauth2client.file import Storage
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

import ApiAuth


def csv_reader():
    path = str(input())
    while True:
        if path[-4:] == '.csv':
            try:
                csv_file = open(path)
                break
            except OSError:
                print('You have entered the unexisting path')
                print('Please provide a path to the CSV files with stock names: ')
                path = str(input())
                continue
        else:
            print('The file path did not lead to csv file')
            print('Please re-enter the path: ')
            path = str(input())
            continue
    csv_read = csv.reader(csv_file)
    stocks = [item for sublist in list(csv_read) for item in sublist]
    return stocks


while True:
    print('Please specify if you want to enter stock names or stock symbols')
    print('Enter 1 for stock names, 2 for stock symbols, 3 to quit: ')
    f = input()
    if f == 1:
        print('Would you like to enter stock names manually or use CSV file?')
        print('Enter 1 to enter stock names manually, 2 to load from file: ')
        f = input()
        if f == 1:
            print('Please enter the stock names separated by space')
            stocks = [i for i in input().split()]
            break
        elif f == 2:
            stocks = csv_reader()
        else:
            print('Please choose from 1 or 2')
            continue
    elif f == 2:
        print('Would you like to enter stock names manually or use CSV file?')
        print('Enter 1 to enter stock names manually, 2 to load from file: ')
        f = input()
        if f == 1:
            print('Please enter the stock symbols separated by space')
            stock_symbols = [i for i in input().split()]
        elif f == 2:
            stock_symbols = csv_reader()
        else:
            print('Please choose from 1 or 2')
            continue
    elif f == 3:
        break
    else:
        print('You have entered wrong key')
        continue

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file']

### Get json file form https://console.cloud.google.com
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Stocks'

authInst = ApiAuth.ApiAuth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)
spreadsheet_service = discovery.build('sheets', 'v4', http=http)

def check_dupe(drive_service, spreadsheet_service):
    flag = True
    files = drive_service.files().list().execute().get('files', [])
    for dict in files:
        if dict['name'] == 'Stocks':
            flag = False
    if flag:
        spreadsheet = {'properties': {
                    'title': 'Stocks'
                }
            }
        spreadsheet_service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()

check_dupe(drive_service, spreadsheet_service)