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

def prev_trading_day(date):
    alid_dates = pd.read_csv(symbol+"Readable.csv")['readable'].values.tolist()
    temp = []
    for x in valid_dates:
        x = x[:-9]
        x = dt.datetime.strptime(x, '%Y-%m-%d').date()
        temp.append(x)
    valid_dates = temp

    date = dt.datetime.strptime(date, '%Y-%m-%d').date()
    while not date in valid_dates:
        date = date - dt.timedelta(days=1)

#Set of classes which will simulate a portfolio and the stockmarket

#Contains the historical and attribute information of any stock in the BZ API
class Stock():
    #Attributes:
    __symbol = None
    __start_date = None
    __end_date = None
    __readable = None

    #Constructor
    def __init__(self, symbol, start_date='yesterday', end_date='today'):
        web.import_readable(symbol)
        df = pd.read_csv(symbol+"Readable.csv")
        df.set_index('readable', inplace=True)
        df = df.loc[next_trading_day(start_date):last_trading_day(end_date)+1]

        self.__readable = df
        self.__symbol = symbol
        self.__start_date = start_date
        self.__end_date = end_date

    #Methods
    def get_symbol(self):
        return self.__symbol

    def get_start_date(self):
        return self.__start_date

    def get_end_date(self):
        return self.__end_date

    def get_readable(self):
        return self.__readable

stock = Stock('aapl')

#Contains the worth and components of a particular stock portfolio
class Portfolio():
    pass
