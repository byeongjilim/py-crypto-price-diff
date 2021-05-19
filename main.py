#! /usr/bin/python
import importlib
import time
import schedule

api = importlib.import_module('api')
dbh = importlib.import_module('databasehandle')

# Hardcoded values - will be made adjustable in the future.
coins = ['BTC', 'ETH', 'XLM', 'XRP']
fees = {
    'BTC': 0.005,
    'ETH': 0.03,
    'XLM': 0.005,
    'XRP': 0.02
}
exchanges = ['bitstamp', 'gopax', 'upbit']
amount = 1000000


def get_data():
    data = {}

    data['bitstamp'] = api.get_bitstamp_data(coins)
    data['gopax'] = api.get_gopax_data(coins)
    data['upbit'] = api.get_upbit_data(coins)

    return data


def save_to_db(data, difference):
    con = dbh.sql_connect()
    for exchange in exchanges:
        dbh.save_data(con, data[exchange], exchange, coins)

    dbh.save_data(con, difference['upbit'], 'diffUpbit', coins)
    dbh.save_data(con, difference['gopax'], 'diffGopax', coins)
    dbh.sql_close(con)


def repeat_job():
    data = get_data()
    difference = calc_diff(data)
    save_to_db(data, difference)


def calc_diff(data):
    bitstamp = data['bitstamp']
    gopax = data['gopax']
    upbit = data['upbit']
    result = {'upbit': {}, 'gopax': {}}
    calculated_fees = {}
    for coin in coins:
        calculated_fees[coin] = bitstamp[coin] * \
            fees[coin] + (10 * api.get_euro())
        result['gopax'][coin] = round(
            (1 / bitstamp[coin] * (amount - calculated_fees[coin])) / (1 / gopax[coin] * amount) * 100000)
        result['upbit'][coin] = round(
            (1 / bitstamp[coin] * (amount - calculated_fees[coin])) / (1 / upbit[coin] * amount) * 100000)
    return result
    # Remember that results are 1000 times what they should be. To get the percentage, divide by 1000


repeat_job()
schedule.every(2).minutes.do(repeat_job)

while True:
    schedule.run_pending()
    time.sleep(1)
