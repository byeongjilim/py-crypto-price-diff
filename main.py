#! /usr/bin/python
import importlib
import time
import schedule
# from win10toast import ToastNotifier
import api
import databasehandle as dbh
# import notificationhandle as notif

# Hardcoded values - will be made adjustable in the future.
coins = ['XLM', 'XRP']
fees = {
    'XLM': 0.005,
    'XRP': 0.02
}
exchanges = ['bitstamp', 'gopax', 'upbit']
amount = 1000000

# sent_not_today = False

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
#        if result['gopax'][coin] / 1000 > 108:
#            if sent_not_today == False:
#                notif.send_notif(result['gopax'][coin] / 1000, '고팍스')
#                sent_not_today = True
#        if result['upbit'][coin] / 1000 > 108:
#                notif.send_notif(result['upbit'][coin] / 1000, 'Upbit')
#                sent_not_today = True
        print("GOPAX " + coin + " " + str(result['gopax'][coin] / 1000) + "%")
        print("Upbit " + coin + " " + str(result['upbit'][coin] / 1000) + "%")
    return result
    # Remember that results are 1000 times what they should be. To get the percentage, divide by 1000




repeat_job()
schedule.every(2).minutes.do(repeat_job)

while True:
    schedule.run_pending()
    time.sleep(1)
