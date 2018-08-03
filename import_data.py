
# 1. Takes data from various sources on the web
# 2. Formats data (pandas dataframe)
# 3. Exports data to pdf

#import statements here
import requests, json, sys, os, warnings
import pandas as pd
import datetime as dt
import numpy as np
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
