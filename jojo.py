from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import tools, file, client
from oauth2client.file import Storage
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

import ApiAuth

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