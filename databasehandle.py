import sqlite3
from sqlite3 import Error


def sql_connect():
    try:
        con = sqlite3.connect('database.db')
        return con

    except Error:
        print(Error)


def create_table(con, table_name):
    cursorObj = con.cursor()
    cursorObj.execute('CREATE TABLE IF NOT EXISTS ' + table_name +
                      '(btc integer, eth integer, xrp integer, xlm integer, time text unique)')
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
    cursorObj.execute('insert into ' + table_name +
                      ' values(?, ?, ?, ?, ?)', data)

    con.commit()
    cursorObj.close()
