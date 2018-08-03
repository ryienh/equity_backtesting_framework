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
def readable_data_exists(ticker):
    if not isinstance(ticker, str):
        raise TypeError('Ticker must be passed as string.')
    ticker = ticker.lower()
    if os.path.isfile(ticker+'Readable.csv'):
        return True
    return False

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
        #if not readable_data_exists:
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
    def price_open(self, date):
        x = self.__readable.at[next_trading_day(self.__symbol, date), 'open']
        return x
    def price_close(self, date):
        x = self.__readable.at[next_trading_day(self.__symbol, date), 'close']
        return x
    def percent_change(self, begin, end=None):
        if end == None:
            price_1 = self.__readable.at[next_trading_day(self.__symbol, begin), 'open']
            price_2 = self.__readable.at[next_trading_day(self.__symbol, begin), 'close']
            pc_change = (price_2 - price_1)/price_1
            return pc_change
        else:
            price_1 = self.__readable.at[next_trading_day(self.__symbol, begin), 'open']
            price_2 = self.__readable.at[prev_trading_day(self.__symbol, end), 'close']
            pc_change = (price_2 - price_1)/price_1
            return pc_change

#Contains the worth and components of a particular stock portfolio
class Portfolio():
    #Attributes
    __start_cash = None
    __current_cash = None
    __stocks_owned = None
    __number_of_trades = None

    #Constructor
    def __init__(self, start_cash):
        self.__start_cash = start_cash
        self.__current_cash = start_cash
        self.__number_of_trades = 0
        self.__stocks_owned = {}

    #Methods
    def get_start_cash(self):
        return self.__start_cash
    def get_current_cash(self):
        return self.__current_cash
    def get_stocks_owned(self):
        return self.__stocks_owned
    def get_number_of_trades(self):
        return self.__number_of_trades

    def buy_stock_at_close(self, stock, date, n):
        cost = stock.price_close(date) * n
        if cost > self.__current_cash:
            raise ValueError('Stock too expensive')
        else:
            self.__current_cash -= cost

            stock_name = stock.get_symbol()
            if not stock_name in self.__stocks_owned or self.__stocks_owned[stock_name] == 0:
                self.__stocks_owned[stock.get_symbol()] = n
            else:
                self.__stocks_owned[stock.get_symbol()] += n

            if n > 0:
                self.__number_of_trades += 1
    def sell_stock_at_close(self, stock, date, n):
        cost = stock.price_close(date) * n
        self.__current_cash += cost
        self.__stocks_owned[stock.get_symbol()] = self.__stocks_owned[stock.get_symbol()] - n
        if self.__stocks_owned[stock.get_symbol()] == 0:
            del self.__stocks_owned[stock.get_symbol()]
        if n > 0:
            self.__number_of_trades += 1
    def buy_stock_at_open(self, stock, date, n):
        cost = stock.price_open(date) * n
        if cost > self.__current_cash:
            raise ValueError('Stock too expensive')
        else:
            self.__current_cash -= cost

            stock_name = stock.get_symbol()
            if not stock_name in self.__stocks_owned or self.__stocks_owned[stock_name] == 0:
                self.__stocks_owned[stock.get_symbol()] = n
            else:
                self.__stocks_owned[stock.get_symbol()] += n

            if n > 0:
                self.__number_of_trades += 1
    def sell_stock_at_open(self, stock, date, n):
        cost = stock.price_open(date) * n
        self.__current_cash += cost
        self.__stocks_owned[stock.get_symbol()] = self.__stocks_owned[stock.get_symbol()] - n
        if self.__stocks_owned[stock.get_symbol()] == 0:
            del self.__stocks_owned[stock.get_symbol()]
        if n > 0:
            self.__number_of_trades += 1
    def buy_max_possible_at_close(self, stock, date):
        n = self.__current_cash // stock.price_close(date)
        self.buy_stock_at_close(stock, date, int(n))
    def buy_max_possible_at_open(self, stock, date):
        n = self.__current_cash // stock.price_open(date)
        self.buy_stock_at_open(stock, date, int(n))
    def cash_out_at_close(self, date):
        static_stocks_owned = self.__stocks_owned.copy().items()
        for key, value in static_stocks_owned:
            key = Stock(key, date, date)
            self.sell_stock_at_close(key, date, value)
    def cash_out_at_open(self, date):
        static_stocks_owned = self.__stocks_owned.copy().items()
        for key, value in static_stocks_owned:
            key = Stock(key, date, date)
            self.sell_stock_at_open(key, date, value)
