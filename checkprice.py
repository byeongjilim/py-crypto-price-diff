#! /usr/bin/python

import requests


def get_data(url):
    return requests.get(url).json()


# EUR 환율 API Call
eur = int(get_data(
    'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWEUR')[0]['cashBuyingPrice'])

# Fees = [6.41 EURs]
fee = eur * 10.41

# Coins
coins = ['BTC', 'ETH', 'XRP', 'LTC']


# 업비트 가격 API Call
def get_upbit_prices():
    url = 'https://api.upbit.com/v1/ticker?markets=KRW-'
    arr = {}
    for i in range(len(coins)):
        price = get_data(url + coins[i])
        arr[coins[i]] = int(price[0]['trade_price'])
    return arr


# 고팍스 가격 API Call
def get_gopax_prices():
    url = 'https://api.gopax.co.kr/trading-pairs/'
    arr = {}
    for i in range(len(coins)):
        price = get_data(url+coins[i]+'-KRW/ticker')
        arr[coins[i]] = int(price['price'])
    return arr


# Bitstamp Prices API Call
def get_bitstamp_prices():
    url = 'https://www.bitstamp.net/api/v2/ticker/'
    arr = {}
    for i in range(len(coins)):
        price = get_data(url+coins[i].lower()+'eur')
        arr[coins[i]] = float(price['last'])
    for i in range(len(coins)):
        arr[coins[i]] *= eur
        arr[coins[i]] = int(arr[coins[i]])
    return arr


# Fee calculating function
def calc_fee(price, fee_size):
    return (fee_size * price + 10 * eur)


# Percentage Difference Function
def calc_per(kor, bit, amount, fee):
    return round((1 / bit * (amount - fee)) / (1 / kor * amount) * 100000) / 1000


# Main Function -- Where the Program Starts
def main():
    prices = {
        'upbit': get_upbit_prices(),
        'gopax': get_gopax_prices(),
        'bitstamp': get_bitstamp_prices()
    }

    fees = {
        'BTC': calc_fee(prices['bitstamp']['BTC'], 0.005),
        'ETH': calc_fee(prices['bitstamp']['ETH'], 0.03),
        'XRP': calc_fee(prices['bitstamp']['XRP'], 0.02),
        'LTC': calc_fee(prices['bitstamp']['LTC'], 0.001),
    }

    print(fees)

    amount = 1000000
    for i in range(len(coins)):
        print("업비트"+coins[i]+":", calc_per(prices['upbit']
              [coins[i]], prices['bitstamp'][coins[i]], amount, fee), "%")
        print("고팍스"+coins[i]+":", calc_per(prices['gopax']
              [coins[i]], prices['bitstamp'][coins[i]], amount, fee), "%")


if __name__ == "__main__":
    main()
