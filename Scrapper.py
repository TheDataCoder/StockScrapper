import requests
import matplotlib as plt
from bs4 import BeautifulSoup

url = 'https://finance.yahoo.com/'
resp = requests.get(url)

soup = BeautifulSoup(resp.text, 'html.parser')

class Stocks:

    def scrap(self, stocks:list):
        """
        Scrap the stock prices for selected period and save them in a list
        :return:
        """
        pass

    def write_cloud(self):
        """
        Upload the scrapped data to google docks spreadsheet
        :return:
        """
        pass

    def plot(self):
        """
        Plot the graph of stock price changes
        :return:
        """
        pass

    def set_limit(self):
        """
        Change colors according to price fluctuations
        :return:
        """
        pass

