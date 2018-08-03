'''
Simple algorithm which demonstrates the use of several features in the
backtesting framework
'''

#Import framework
import market

#Make a portfolio
my_portfolio = market.Portfolio(10000)
print(my_portfolio.get_stocks_owned())
print(my_portfolio.get_start_cash())
print(my_portfolio.get_current_cash())
print(my_portfolio.get_number_of_trades())
print('\n')

#Inititalize stocks
aapl = market.Stock('aapl', '2013-01-01', '2018-06-19')
snap = market.Stock('snap', '2013-01-01', '2018-06-19')

#Buy stock
my_portfolio.buy_stock_at_close(snap, '2017-12-02', 12)
print(my_portfolio.get_stocks_owned())
print(my_portfolio.get_start_cash())
print(my_portfolio.get_current_cash())
print(my_portfolio.get_number_of_trades())
print('\n')

my_portfolio.buy_max_possible(aapl, '2018-01-05')
print(my_portfolio.get_stocks_owned())
print(my_portfolio.get_start_cash())
print(my_portfolio.get_current_cash())
print(my_portfolio.get_number_of_trades())
print('\n')

#Sell stock
my_portfolio.sell_stock_at_close(snap, '2018-03-04', 2)
print(my_portfolio.get_stocks_owned())
print(my_portfolio.get_start_cash())
print(my_portfolio.get_current_cash())
print(my_portfolio.get_number_of_trades())
print('\n')

my_portfolio.cash_out('2018-06-18')
print(my_portfolio.get_stocks_owned())
print(my_portfolio.get_start_cash())
print(my_portfolio.get_current_cash())
print(my_portfolio.get_number_of_trades())
print('\n')
