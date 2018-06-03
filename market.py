import pandas as pd
import datetime as dt

import import_data as web

#helper functions:

#date must be in format yyyy-mm-dd
def next_trading_day(symbol, date):
    valid_dates = pd.read_csv(symbol+"Readable.csv")['readable'].values.tolist()
    temp = []
    for x in valid_dates:
        x = x[:-9]
        x = dt.datetime.strptime(x, '%Y-%m-%d').date()
        temp.append(x)
    valid_dates = temp

    date = dt.datetime.strptime(date, '%Y-%m-%d').date()
    while not date in valid_dates:
        date = date + dt.timedelta(days=1)
    return str(date)
def prev_trading_day(symbol, date):
    valid_dates = pd.read_csv(symbol+"Readable.csv")['readable'].values.tolist()
    temp = []
    for x in valid_dates:
        x = x[:-9]
        x = dt.datetime.strptime(x, '%Y-%m-%d').date()
        temp.append(x)
    valid_dates = temp

    date = dt.datetime.strptime(date, '%Y-%m-%d').date()
    while not date in valid_dates:
        date = date - dt.timedelta(days=1)
    return str(date)

#Set of classes which will simulate a portfolio and the stockmarket

#Contains the historical and attribute information of any stock in the BZ API
class Stock():
    #Attributes:
    __symbol = None
    __start_date = None
    __end_date = None
    __readable = None

    #Constructor
    def __init__(self, symbol, start_date, end_date):
        web.import_readable(symbol)
        df = pd.read_csv(symbol+"Readable.csv")

        new_dates = df['readable'].values.tolist()
        temp = []
        for date in new_dates:
            date = date[:-9]
            temp.append(date)
        new_dates = temp
        df['readable'] = new_dates

        df.set_index('readable', inplace=True)
        df = df.loc[next_trading_day(symbol, start_date):prev_trading_day(symbol, end_date)]

        self.__readable = df
        self.__symbol = symbol
        self.__start_date = next_trading_day(symbol, start_date)
        self.__end_date = prev_trading_day(symbol, end_date)

    #Methods
    def get_symbol(self):
        return self.__symbol
    def get_start_date(self):
        return self.__start_date
    def get_end_date(self):
        return self.__end_date
    def get_readable(self):
        return self.__readable
    def percent_change(self, begin, end=None):
        if end == None:
            print(self.__symbol)
            price_1 = self.__readable.at[next_trading_day(self.__symbol, begin), 'open']
            price_2 = self.__readable.at[next_trading_day(self.__symbol, begin), 'close']
            pc_change = (price_2 - price_1)/price_1
            return pc_change

apple = Stock(symbol='aapl', start_date='2017-01-01', end_date='2018-01-01')
print(apple.percent_change('2017-02-02'))

#Contains the worth and components of a particular stock portfolio
class Portfolio():
    pass
