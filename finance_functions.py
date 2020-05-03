'''
    Aneesha Sreerama
    Alexander Deris
    DS2000
    Semester Project
'''

import requests
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
from nytimesarticle import articleAPI

ALPHA_KEY = '6U1UQUODV2YQFLEB'
alpha_vantage_url = 'https://www.alphavantage.co/query'

def stock_data(symbol):
    ''' Function: stock_data
        Parametrs: ticker symbol (String)
        Returns: response from API request (JSON)
    '''

    
    data = { 'function': 'TIME_SERIES_MONTHLY_ADJUSTED',
             'symbol': symbol,
             'datatype': 'json',
             'apikey' : ALPHA_KEY}
    response = requests.get(alpha_vantage_url, data)
    response_json = response.json()

    return response_json
    

def stock_df(response):
    ''' Function: stock_df
        Parameters: response from the API request (JSON)
        Returns: DataFrame formed using the response (Pandas)
    '''

    data = pd.DataFrame.from_dict(response['Monthly Adjusted Time Series'], orient= 'index').sort_index(axis=1)
    data = data.rename(columns={ '1. open': 'Open', '2. high': 'High', '3. low': 'Low',
                                 '4. close': 'Close', '5. adjusted close' : 'Adjusted Close',
                                 '6. volume': 'Volume', '7. dividend amount' : 'Divident Amount'})
    return data

def all_dates(response):
    ''' Function: all_dates
        Parameters: response from the API request (JSON)
        Returns: The dates used as the index in the response (List)
    '''

    dates = response['Monthly Adjusted Time Series'].keys()
    dates = list(dates)

    return dates

def monthly_change(data):
    ''' Function: monthly_change
        Parameters: DataFrame formed using the response (Pandas)
        Returns: The difference between opening and closing price of the stock
                 for the month (List)
    '''

    monthly_change = []
    for ind in data.index:
        closing = float(data['Close'][ind])
        opening = float(data['Open'][ind])
        change = round(closing - opening, 3)
        monthly_change.append(change)

    return monthly_change

def dividents(data):
    ''' Function: dividents
        Parameter: DataFrame formed using the response (Pandas)
        Returns: The reported divident for each month (List)
    '''
    
    all_dividents = []
    for ind in data.index:
        divident = float(data['Divident Amount'][ind])
        all_dividents.append(divident)

    return all_dividents

def quarterly_dividents(all_dividents):
    ''' Function: dividents
        Parameter: The reported divident for each month (List)
        Returns: The reported divident for each quarter (List)
    '''
        
    quarterly_dividents = all_dividents
    quarterly_dividents.pop(0)
    quarterly_dividents = quarterly_dividents[::3]

    return quarterly_dividents

def pos_or_neg(change):
    ''' Function: pos_or_neg
        Parameter: The change in the stock market for each month (List)
        Returns: If the stock increased (1) or decresed(0) (List)
    '''

    for i in range(len(change)):
        if change[i] > 0:
            change[i] = 1
        else:
            change[i] = 0

    return change
        


def testing():
    
    # Calls the ALPHA VANTAGE API to retreive financial data regarding Apple
    response = stock_data('AAPL')

    # Converts the JSON data into a dataframe
    APPLE_DF = stock_df(response)
    print(APPLE_DF)

    # Converts all the dictionary keys into a list
    DATES = all_dates(response)
    print(DATES)

    # Reports how the value of the stock changed that month
    MONTHLY_CHANGE = monthly_change(APPLE_DF)
    print(MONTHLY_CHANGE)

    # Tells whether the stock increased or decreased during the month
    BINARY_CHANGE = pos_or_neg(MONTHLY_CHANGE)
    print(BINARY_CHANGE)

    # Reports the earnings for every month/quarter
    DIVIDENTS = dividents(APPLE_DF)
    QUARTERLY = quarterly_dividents(DIVIDENTS)

testing()



