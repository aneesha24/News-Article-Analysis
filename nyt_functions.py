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
from csv import writer
import csv
import time
    
NYT_KEY = '7UoMcE8X2msruu0A1odn6CiA24VlIIkb'
new_york_times_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"


def apple_data(start_date, end_date):
    ''' Functions: apple_data
        Parameters: a start date for the search filter (String)
                    an end date for the search filter (String)
        Return: the response to the API request (JSON)
    '''

    filters = {'q': 'APPLE',
                   'news_desk': ('Business' 'Technology'),
                   'sort': 'relevance',
                   'begin_date': start_date, #format of the data: yyyymmdd
                   'end_date': end_date, #format of the data: yyyymmdd
                   'api-key': NYT_KEY}

    articles = requests.get(new_york_times_url, params=filters)
    articles = articles.json()

    return articles

def input_data(articles):
    ''' Functions: input_data
        Parameters: response to the API request (JSON)
        Return: none
        Does: Extracts the date, headline, and article from each
              of the 10 articles and appends them to a CSV file
    '''    

    for j in range(10):

        headline = str(articles['response']['docs'][j]['headline']['main'])
        abstract = str(articles['response']['docs'][j]['abstract'])
        date = str(articles['response']['docs'][j]['pub_date'][:10])

        with open('informations.csv', 'a+', newline='') as in_file:
            csv_writer = writer(in_file)
            csv_writer.writerow([date, headline, abstract])


def get_date(i):
    ''' Function: get_date
        Parameters: any arbitrary number (int)
        Returns: a start date for the search filter (String)
                 an end date for the search filter (String)
        Does: Formats the date based on the number of months
              past March 2000
    '''
        
    year = int((i + 3) / 12)
    month = ((i + 3) % 12) + 1
    
    if month % 2 == 1 and month <= 7:
        day = '31'
    elif month == 8 or month == 10 or month == 12:
        day = '31'
    elif month == 2 & year % 4 == 0:
        day = '29'
    elif month == 2:
        day = '28'
    else:
        day = '30'

    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)

    start_date = str(2000 + year) + month + '01'
    end_date = str(2000 + year) + month + day

    time.sleep(30)

    return (start_date, end_date)

          
def testing():
    
    # This analysis of Apple is from years April 2000 - March 2020 and
    # will be using 240 months worth of data
    for i in range(240):

        # Gets the formatted start and end date for the API request
        date = get_date(i)
        print(date)

        # Extracts the start and end dates
        start = date[0]
        end = date[1]

        # Calls the NEW YORK TIMES API for data regarding articles
        articles = apple_data(start, end)

        # Inputs the data into a CSV file
        input_data(articles)
        print('Completed!')

#testing()
        
        

            
        
        

        
        
        










        
