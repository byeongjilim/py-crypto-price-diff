import sqlite3
from sqlite3 import Error
from datetime import datetime


def sql_connect():
    """ Connect / Load database file. """
    try:
        con = sqlite3.connect('database.db')
        return con

    except Error:
        print(Error)


def create_table(con, table_name, coins):
    cursorObj = con.cursor()
    value_str = '('
    for coin in coins:
        value_str += coin + ' integer, '
    value_str += 'time text unique)'
    cursorObj.execute('CREATE TABLE IF NOT EXISTS ' + table_name +
                      value_str)
    con.commit()
    cursorObj.close()


def get_data(con, table_name):
    cursorObj = con.cursor()
    cursorObj.execute('select * from ' + table_name)
    data = cursorObj.fetchall()
    return data


def save_data(con, data, table_name, coins):
    create_table(con, table_name, coins)
    cursorObj = con.cursor()
    value_str = ' values('
    coin_str = '('
    parsed_data = []
    for coin in coins:
        value_str += '?,'
        coin_str += coin + ','
        parsed_data.append(data[coin])
    coin_str += 'time) '
    value_str += '?)'
    now = datetime.now()
    parsed_data.append(now.strftime("%Y/%m/%d, %H:%M"))
    result = 'insert into ' + table_name + coin_str + value_str
    print(result)
    cursorObj.execute(result, parsed_data)

    con.commit()
    cursorObj.close()


def sql_close(con):
    con.close()
