
# 1. Takes data from various sources on the web
# 2. Formats data (pandas dataframe)
# 3. Exports data to pdf

#import statements here
import requests, json, sys, os, warnings
import pandas as pd
import datetime as dt
import numpy as np


#REQUIRES: Valid ticker, range and interval
#MODIFIES: Exports csv to local directory - 3 columns, numerical index,
#key and value
#RETURNS: Nothing
def import_live_data(ticker, range='6y', interval='1D'):
    #import chart live from web
    url = 'https://data.benzinga.com/rest/v2/quote?symbols='+ticker.upper()
    data = requests.get(url)
    #format data
    data = data.json()
    data = data[ticker.upper()]
    #handle for invalid ticker
    try:
        df = pd.DataFrame.from_dict(data, orient='index')
    except AttributeError:
        warnings.warn(('Must imput valid ticker. Try Again. %s not available.' % (ticker)))
        return
    #send to csv
    df.reset_index(inplace=True)
    df.columns = ['key', 'value']
    df.to_csv(ticker.lower() + 'LiveData.csv')

#REQUIRES: Valid ticker, range and interval
#MODIFIES: Exports csv to local directory - index, close, dateTime, high,
#low, open, time, volume
#RETURNS: Nothing
def import_ohlc(ticker, range='6y', interval='1D'):
    #import chart data from web
    url = 'https://data.benzinga.com/rest/v2/chart?symbol='+ticker.upper()+'&from='+range+'&interval='+interval
    data = requests.get(url)
    data = data.json()
    #format data
    try:
        data = data['candles']
    except KeyError:
        raise ValueError('Must imput valid ticker. Try Again.')
    df = pd.DataFrame(data)
    df = df.fillna(method='ffill')
    #send to csv
    df.to_csv(ticker.lower() + 'OHLC.csv')

#REQUIRES: Valid ticker, range and interval
#MODIFIES: Exports csv to local directory - when calc_technicals is false:
#readable, close, high, low, open, volume
#when on, includes 100ma, 20ma, MA_diff, range, labels, rsi
#RETURNS: Nothing
def import_readable(ticker,range='6y',interval='1D',calc_technicals=False):
    #import chart data from web
    url = 'https://data.benzinga.com/rest/v2/chart?symbol='+ticker.upper()+'&from='+range+'&interval='+interval
    data = requests.get(url)
    data = data.json()
    #format data
    try:
        data = data['candles']
    except KeyError:
        warnings.warn('Must imput valid ticker. Stock %s failed to import.' % (ticker))
        return
    df = pd.DataFrame(data)
    df = df.fillna(method='ffill')

    #add readable dates
    readable = []
    try:
        timestamps = df["time"].values.tolist()
    except KeyError:
        warnigns.warn('Could not import %s.Readable.csv' % (ticker))
        return
    for stamp in timestamps:
        stamp = int(stamp*.001)
        stamp = dt.datetime.fromtimestamp(stamp)
        readable.append(stamp + dt.timedelta(days=1))

    #reformat
    df["readable"] = readable
    df.drop(["time", "dateTime"], axis=1, inplace=True)
    df.set_index("readable", inplace=True)

    #calculate technicals if necessary
    if calc_technicals == True:
        #MA_diff feature
        df['100ma'] = df['close'].rolling(window=100, min_periods=0).mean() #add 100 ma
        df['20ma'] = df['close'].rolling(window=20, min_periods=0).mean()
        #closed="right" can be passed as a paramater in above two functions (rolling)
        df['MA_diff'] = df['20ma'] - df['100ma']
        #range diff
        df['range'] = df['high'] - df['low']
        #generate labels (in this case whether the stock went up or down)
        df['price diff'] = df['close'] - df['open']
        df['labels'] = np.where(df['price diff'] >= 0, 1, 0)
        #generate and add rsi feature
        delta = df['price diff']
        dUp, dDown = delta.copy(), delta.copy()
        dUp[dUp < 0] = 0
        dDown[dDown > 0] = 0

        RolUp = pd.Series.rolling(dUp, 14, closed = "right").mean()
        RolDown = pd.Series.rolling(dDown, 14, closed = "right").mean().abs()

        RS = RolUp / RolDown
        RSI = 100 - (100/(1 + RS))
        df['rsi'] = RSI
    #send to csv
    df.to_csv(ticker.lower() + 'Readable.csv')

#REQUIRES: Valid ticker, start and end dates as strings formatted YYYY-MM-DD
#MODIFIES: Exports csv to local directory - date, action_company, action_pt, analyst,
#pt_current, pt_prior, rating_current, rating_prior, time, analyst_name
#RETURNS: Nothing
def import_ratings(ticker, start, end):
    #check for correctly formatted date
    check_start = start.split('-')
    if len(check_start[0]) != 4 or len(check_start[1]) != 2 or len(check_start[2]) != 2:
        raise ValueError('Start date for import_ratings not formatted correctly. Use yyyy-mm-dd')
    if int(check_start[0]) < 1950 or int(check_start[0]) > int(dt.date.today().strftime('%Y')):
        raise ValueError('Invalid year. Try again. Format should be YYYY and be no older than 1950')
    if int(check_start[1]) > 12 or int(check_start[1]) < 0:
        raise ValueError('Invalid month. Try again. Format should be MM.')
    if int(check_start[2]) > 31 or int(check_start[2]) < 1:
        raise ValueError('Invalid day. Try again. Format should me DD.')
    check_end = end.split('-')
    if len(check_end[0]) != 4 or len(check_end[1]) != 2 or len(check_end[2]) != 2:
        raise ValueError('Start date for import_ratings not formatted correctly. Use yyyy-mm-dd')
    if int(check_end[0]) < 1950 or int(check_end[0]) > int(dt.date.today().strftime('%Y')):
        raise ValueError('Invalid year. Try again. Format should be YYYY and be no older than 1950')
    if int(check_end[1]) > 12 or int(check_end[1]) < 0:
        raise ValueError('Invalid month. Try again. Format should be MM.')
    if int(check_end[2]) > 31 or int(check_end[2]) < 1:
        raise ValueError('Invalid day. Try again. Format should me DD.')
    #import data from web
    headers = {'accept': 'application/json'}
    params = {'token': '899efcbfda344e089b23589cbddac62b', 'parameters[date_from]': start, \
    'parameters[date_to]': end, 'parameters[tickers]': ticker.upper()}
    ratingsUrl = "https://api.benzinga.com/api/v2/calendar/ratings/"
    ratings = requests.get(ratingsUrl, headers=headers, params=params)
    #format data
    ratings = ratings.json()
    try:
        ratings = ratings['ratings']
        df = pd.DataFrame(ratings)
        df.set_index('date', inplace=True)
        df = df.iloc[::-1]
        df = df[['action_company', 'action_pt', 'analyst', 'pt_current', \
        'pt_prior', 'rating_current', 'rating_prior', 'time', 'analyst_name']]
        #send to csv
        df.to_csv(ticker.lower() + 'Ratings.csv')
    except TypeError:
        warnings.warn('%s - Either invalid ticker or no available ratings for time period' % (ticker))
        return


#REQUIRES: Nothing
#MODIFIES: Removes csv files from directory it is called from
#RETURNS: Success message (optional)
def remove(printvar=False):
    dir = [f for f in os.listdir('.') if os.path.isfile(f)]

    for file in dir:
        if file.endswith(".csv") and file != "constituents.csv" and file != "sp500Ratings.csv":
            os.remove(file)
    if printvar == True:
        print("Files Deleted!")
# remove(printvar=False)




#NOTE: Archive
# def import_data(call=False, tick='', range = "5y", interval = "1d", ingest=False, rstart = '2017-01-01', rend = '2017-12-31', fast=False, years=5):
#     #set variables
#     if call == True:
#         ticker = tick
#     if call == False and len(sys.argv) == 1:
#         ticker = "aapl"
#     if call == False and len(sys.argv) == 2:
#         ticker = sys.argv[1].lower()
#
#     #get data from web:
#     ticker = ticker.upper()
#     url = "https://data.benzinga.com/rest/v2/quote?symbols="+ticker
#     response = requests.get(url)
#
#     url2 = "https://data.benzinga.com/rest/v2/chart?symbol="+ticker+"&from="+range+"&interval="+interval
#     response2 = requests.get(url2)
#
#     #format to pandas df
#     data = response.json()
#     data = data[ticker]
#     df = pd.DataFrame.from_dict(data, orient="index")
#
#     data2 = response2.json()
#     data2 = data2["candles"]
#     df2 = pd.DataFrame(data2)
#     #fix NaN issue:
#     df2 = df2.fillna(method='ffill')
#
#
#     df3 = df2
#     readable = []
#     timestamps = df3["time"].values.tolist()
#     for stamp in timestamps:
#         stamp = int(stamp*.001)
#         stamp = dt.datetime.fromtimestamp(stamp)
#         readable.append(stamp + dt.timedelta(days=1))
#
#     #Add dates and features
#     df3["readable"] = readable
#     df3.drop(["time", "dateTime"], axis=1, inplace=True)
#     df3.set_index("readable", inplace=True)
#
#
#     if fast == False:
#         #MA_diff feature
#         df3['100ma'] = df3['close'].rolling(window=100, min_periods=0).mean() #add 100 ma
#         df3['20ma'] = df3['close'].rolling(window=20, min_periods=0).mean()
#         #closed="right" can be passed as a paramater in above two functions (rolling)
#         df3['MA_diff'] = df3['20ma'] - df3['100ma']
#         #range diff
#         df3['range'] = df3['high'] - df3['low']
#         #generate labels (in this case whether the stock went up or down)
#         df3['price diff'] = df3['close'] - df3['open']
#         df3['labels'] = np.where(df3['price diff'] >= 0, 1, 0)
#         #generate and add rsi feature
#         delta = df3['price diff']
#         dUp, dDown = delta.copy(), delta.copy()
#         dUp[dUp < 0] = 0
#         dDown[dDown > 0] = 0
#
#         RolUp = pd.Series.rolling(dUp, 14, closed = "right").mean()
#         RolDown = pd.Series.rolling(dDown, 14, closed = "right").mean().abs()
#
#         RS = RolUp / RolDown
#         RSI = 100 - (100/(1 + RS))
#         df3['rsi'] = RSI
#
#     #Import ratings data
#     headers = {'accept': 'application/json'}
#     params = {'token': '899efcbfda344e089b23589cbddac62b', 'parameters[date_from]': rstart, \
#     'parameters[date_to]': rend, 'parameters[tickers]': ticker}
#     ratingsUrl = "https://api.benzinga.com/api/v2/calendar/ratings/"
#     ratings = requests.get(ratingsUrl, headers=headers, params=params)
#     ratings = ratings.json()
#     try:
#         ratings = ratings['ratings']
#         df4 = pd.DataFrame(ratings)
#         df4.set_index('date', inplace=True)
#         df4 = df4.iloc[::-1]
#         df4 = df4[['action_company', 'action_pt', 'analyst', 'pt_current', \
#         'pt_prior', 'rating_current', 'rating_prior', 'time', 'analyst_name']]
#     except Exception:
#         pass
#         #print("No ratings data available for " + ticker)
#     #send to csv
#     ticker = ticker.lower()
#     if(ingest == True):
#         df.to_csv("Data/LiveData/" + ticker + "LiveData.csv")
#         #df2.to_csv("Data/OHLC/" + ticker + "OHLC.csv")
#         df3.to_csv("Data/Readable/" + ticker + "Readable.csv")
#         try:
#             df4.to_csv("Data/Ratings/" + ticker + "Ratings.csv")
#         except:
#             pass
#     else:
#         df.to_csv(ticker + "LiveData.csv")
#         #df2.to_csv(ticker + "OHLC.csv")
#         df3.to_csv(ticker + "Readable.csv")
#         try:
#             df4.to_csv(ticker + "Ratings.csv")
#         except:
#             pass

# importData()
