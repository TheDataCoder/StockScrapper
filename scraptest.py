import requests
from bs4 import BeautifulSoup


url = 'https://finance.yahoo.com/quote/6861.T'
resp = requests.get(url)

soup = BeautifulSoup(resp.text, "html.parser")
price = soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text

### pre-market:
### soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('p').find('span').text


