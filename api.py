import requests


def get_json(url):
    return requests.get(url).json()


def get_euro():
    return int(get_json(
        'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWEUR')[0]['cashBuyingPrice'])


def get_exchange_data(url, coins, url_back=''):
    """
    Returns the api call data from the url in object form.
    """
    obj = {}
    for coin in coins:
        tmp_data = get_json(url + coin + url_back)
        obj[coin] = tmp_data
    return obj


def get_upbit_data(coins):
    data = get_exchange_data(
        "https://api.upbit.com/v1/ticker?markets=KRW-", coins)
    result = {}
    for coin in coins:
        result[coin] = int(data[coin][0]['trade_price'])
    return result


def get_gopax_data(coins):
    data = get_exchange_data(
        'https://api.gopax.co.kr/trading-pairs/', coins, '-KRW/ticker')
    result = {}
    for coin in coins:
        result[coin] = int(data[coin]['price'])
    return result


def get_bitstamp_data(coins):
    eur = get_euro()
    lower_coins = coins.copy()
    for i in range(len(coins)):
        lower_coins[i] = lower_coins[i].lower()
    data = get_exchange_data(
        'https://www.bitstamp.net/api/v2/ticker/', lower_coins, 'eur')
    result = {}
    for i in range(len(lower_coins)):
        result[coins[i]] = int(float(data[lower_coins[i]]['last']) * eur)
    return result
