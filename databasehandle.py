import sqlite3
from sqlite3 import Error


def sql_connect():
    try:
        con = sqlite3.connect('database.db')
        return con

    except Error:
        print(Error)


def create_table(con, table_name, coins):
    cursorObj = con.cursor()
    value_str = '('
    for coin in coins:
        value_str += + coin + ' integer, '
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


def save_data(con, data, table_name):
    create_table(con, table_name)
    cursorObj = con.cursor()
    value_str = ' values('
    for _ in data:
        value_str += '?, '
    value_str += ')'
    cursorObj.execute('insert into ' + table_name + value_str, data)

    con.commit()
    cursorObj.close()
