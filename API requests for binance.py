import requests

response = requests.get('https://api.binance.com/api/v3/ticker/price')
coins = response.json()

eth_price = None
btc_price = None


for coin in coins:
    if coin['symbol'] == 'ETHUSDT':
        eth_price = float(coin['price'])

    elif coin['symbol'] == 'BTCUSDT':
        btc_price = float(coin['price'])


print(f"Цена BTC - {int(btc_price)}$")
print(f"Цена ETH - {int(eth_price)}$")

