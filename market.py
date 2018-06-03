import pandas as pd
import datetime as dt

import import_data as web

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
        self.__readable = pd.read_csv(symbol+"Readable.csv")
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


#Contains the worth and components of a particular stock portfolio
class Portfolio():
    pass
