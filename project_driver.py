'''
    Aneesha Sreerama
    Alexander Deris
    DS2000
    Semester Project
'''
import csv
import pandas as pd
import matplotlib.pyplot as plt

from article_functions import abstract_sentiment
from article_functions import headline_category
from finance_functions import stock_data
from finance_functions import stock_df
from finance_functions import all_dates
from finance_functions import monthly_change
from finance_functions import pos_or_neg


def process_file(filename):
    ''' Function: process_file
        Parameter: Name of the file (String)
        Returns: scores for the article (List of Numbers)
        Does: reads data from a CSV file and analyzes the data
    '''
    # Holds the score for each article
    scores = []

    # Holds the 10 headlines the API collected for each month
    headlines = []
    abstracts = []

    with open(filename) as infile:
        csv_contents = csv.reader(infile, delimiter = ',')

        # Extracts the headline and abstract from the CSV file
        counter = 0
        for row in csv_contents:
            counter += 1
            # Appends each headline and abstract to its respective list
            headlines.append(row[1])
            abstracts.append(row[2])

            # Runs a function to categorize the headlines &
            # determine the subject of the contents in the article
            if counter % 10 == 0:
                categories = headline_category(headlines)
                article_score = abstract_sentiment(abstracts, categories)
                scores.append(article_score)

                # Clears the headlines and abstracts lists
                headlines = []
                abstracts = []

    return scores

def accuracy(info, total):
    ''' Function: accuracy
        Parameters: the information dataframe (Pandas)
                    the total number of scores (int)
        Returns: the accuracy of the predictions (Float)
    '''

    accuracy = 0
    for ind in info.index:
        guess = int(info['Article Scores'][ind])
        actual = int(info['Stock Trend'][ind])
        if guess == actual:
            accuracy += 1

    return 100 * (accuracy / total)
    

def main():

    # Obtains the final score after the article analysis for the
    # month's worth of articles
    scores = process_file('information.csv')
    scores.reverse()

    # Changes the score to 1 if positive and to 0 if negative
    BINARY_SCORES = pos_or_neg(scores)
    
    # Calls the ALPHA VANTAGE API to retreive financial data regarding Apple
    response = stock_data('AAPL')

    # Converts the JSON data into a dataframe
    APPLE_DF = stock_df(response)

    # Converts all the dictionary keys into a list
    DATES = all_dates(response)

    # Reports how the value of the stock changed that month
    MONTHLY_CHANGE = monthly_change(APPLE_DF)
     
    # Tells whether the stock increased or decreased during the month
    BINARY_CHANGE = pos_or_neg(MONTHLY_CHANGE)
    
    # Creates a dataframe 
    frame = {'Article Scores': BINARY_SCORES,
             'Stock Trend': BINARY_CHANGE}
    
    info = pd.DataFrame(frame)
    info.index = DATES

    #print("ACCURACY: ", accuracy(info, len(DATES)), "%")


#main()
