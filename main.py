import numpy as np
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set parsing values
symbol = 'BTCUSDT'  # Trading pair
limit = 5000  # Number of orders in the order book

# Request to the Binance API
base_url = 'https://api.binance.com'
endpoint = '/api/v3/depth'
params = {'symbol': symbol, 'limit': limit}
response = requests.get(base_url + endpoint, params=params)
all_bids = 0
all_asks = 0

if response.status_code == 200:
    data = json.loads(response.text)
    bids = data['bids']
    asks = data['asks']
    for _ in range(len(bids)):
        all_bids += float(bids[_][0]) * float(bids[_][1])
    for _ in range(len(asks)):
        all_asks += float(asks[_][0]) * float(asks[_][1])
    ratio = all_bids - all_asks
    print('Ratio', ratio)
    bid_prices = [float(bid[0]) for bid in bids]
    bid_volumes = [float(bid[1]) for bid in bids]
    ask_prices = [float(ask[0]) for ask in asks]
    ask_volumes = [float(ask[1]) for ask in asks]

    # Plot the order book depth chart
    fig, ax = plt.subplots()
    ax.plot(bid_prices, bid_volumes, label='Bids')
    ax.plot(ask_prices, ask_volumes, label='Asks')
    ax.fill_between(bid_prices, bid_volumes, color='green', alpha=0.2)
    ax.fill_between(ask_prices, ask_volumes, color='red', alpha=0.2)
    ax.set_xlabel('Price')
    ax.set_ylabel('Volume')
    ax.set_title(f'{symbol} Order Book Depth Chart')
    ax.legend()
    plt.show()
else:
    print(f'Error, something went wrong: {response.status_code}')


# Request to the Cryptocompare API
crypto_symbol = 'BTC'
currency = 'USDT'
crypto_limit = 30
average_volume = 0
average_volatility = 0
today_volatility = 0

crypto_url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={crypto_symbol}&tsym={currency}&limit={crypto_limit}'

response = requests.get(crypto_url)

if response.status_code == 200:
    data = response.json()['Data']['Data']
    for d in data:
        average_volume += d['volumefrom']
        today_volatility = d['high'] - d['low']
        average_volatility += today_volatility
        # print(f"Date: {datetime.fromtimestamp(d['time'])}, Open: {d['open']}, High: {d['high']}, Low: {d['low']}, "
        #       f"Close: {d['close']}, Volume: {d['volumefrom']}")
    print('Average volume =', average_volume / 30)
    print('Today volume =', d['volumefrom'])
    print('Volume index =', d['volumefrom'] / (average_volume / 30))
    print()
    print('Average volatility =', average_volatility / 30)
    print('Today volatility =', today_volatility)
    print('Volatility index =', today_volatility / (average_volatility / 30))
    dates = [datetime.fromtimestamp(d['time']) for d in data]
    close_prices = [d['close'] for d in data]

    # Plot the historical data
    fig, ax = plt.subplots()
    ax.plot_date(dates, close_prices, '-')
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))
    ax.autoscale_view()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xlabel('Date')
    plt.ylabel(f'{crypto_symbol}/{currency} price (USD)')
    plt.title(f'{crypto_symbol}/{currency} Price History')
    plt.grid()
    plt.show()


else:
    print(f"Error: {response.status_code}")


# Request to the Blockchaincenter
url = "https://www.blockchaincenter.net/altcoin-season-index/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    altseason_index = soup.find("button", class_="nav-link timeselect active").text
    print(f"Индекс альт-сезона: {altseason_index[-3:-1]}")
else:
    print(f"Error, something went wrong: {response.status_code}")


# Request to the Alternative API
alt_url = "https://api.alternative.me/fng/"
alt_params = {
    "limit": 1,
    "format": "json"
}

response = requests.get(alt_url, params=alt_params)

if response.status_code == 200:
    data = json.loads(response.text)
    fear_greed_index = data['data'][0]['value']
    index_classification = data['data'][0]['value_classification']
    print(f"Fear and Greed Index: {fear_greed_index} ({index_classification})")
else:
    print(f"Error, something went wrong: {response.status_code}")


# Request to the Instaforex

url = "https://www.instaforex.com/ua/chart/usdx?code=overview&account=standard"

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    index_usd = soup.find("span", class_='#USDXask').text
    print(f"Курс индекса доллара: {index_usd}")
else:
    print(f"Error, something went wrong: {response.status_code}")


url = "https://www.instaforex.com/ua/chart/spx?code=overview&account=standard"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    index_snp = soup.find("span", class_='#SPXask').text
    print(f"Текущее значение индекса S&P 500: {index_snp}")
else:
    print(f"Error, something went wrong: {response.status_code}")


url = "https://www.instaforex.com/ua/chart/gold?code=overview&account=standard"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    price_gold = soup.find("span", class_='GOLDask').text
    print(f"Текущая цена золота: {price_gold}")
else:
    print(f"Error, something went wrong: {response.status_code}")


url = "https://www.instaforex.com/ru/chart/silver?code=overview&account=standard"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    price_silver = soup.find("span", class_='SILVERask').text
    print(f"Текущая цена серебра: {price_silver}")
else:
    print(f"Error, something went wrong: {response.status_code}")



