import requests
from bs4 import BeautifulSoup
import pandas as pd

stocks_frame = pd.DataFrame(data = {'Price': [], 'Current price': [], 'Current price timestamp' : []})

url = 'https://finance.yahoo.com/quote/TSLA'
resp = requests.get(url)

soup = BeautifulSoup(resp.text, "html.parser")
price = soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text

#pre-market:
#soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('p').find('span').text
#after hours:
#soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('p').find('span').text

Current = soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('p').text
if 'After hours' or 'Pre-market' in Current:
