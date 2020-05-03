'''
    Aneesha Sreerama
    Alexander Deris
    DS2000
    Semester Project
'''
import csv
import pandas as pd
import matplotlib.pyplot as plt
import turtle

from article_functions import abstract_sentiment
from article_functions import headline_category
from finance_functions import stock_data
from finance_functions import stock_df
from finance_functions import all_dates
from finance_functions import monthly_change
from finance_functions import pos_or_neg
from project_driver import process_file


def get_headlines(filename):
    ''' Function: process_file
        Parameter: Name of the file (String)
        Returns: all the headlines (List of Strings)
        Does: reads data from a CSV file and collects all the headlines
    '''

    with open(filename) as infile:
        csv_contents = csv.reader(infile, delimiter = ',')

        # Extracts the headline and abstract from the CSV file
        headlines = []
        for row in csv_contents:
            headlines.append(row[1])

    return headlines

def headline_visual():
    ''' Function: headline_visual
        Parameter: None
        Returns: None
        Does: reads data from a CSV file and renders a bar graph
              depicting the number of headlines in each category
    '''

    # Gets and categorizes all of the headlines
    headlines = get_headlines('information.csv')
    categories = headline_category(headlines)
    
    # Name of the categories
    cat_names = ['Product Discussion', 'Apple Competitors',
                 'Apple Performance', 'Undescriptive',
                  'Unrelated']
    
    cat_buckets = [0,0,0,0,0]
    
    # Adds 1 to each bucket when an aricle falls in that category
    for i in range(len(categories)):
        num = categories[i]
        cat_buckets[num - 1] += 1

    # Creates a bar graph
    pos = [i for i in range(5)]
    plt.bar(pos, cat_buckets)
    plt.xticks(pos, cat_names)
    plt.ylabel('Number of Articles')
    plt.xlabel('Categories')
    plt.title('Headline Category')
    plt.show()


def monthly_changes():
    ''' Function: monthly_changes
        Parameter: None
        Returns: None
        Does: retrieves Apple data and plots the change in stock
              price for each month
    '''

    # Retrieves the data for Apple and reports the change in stock
    # for the month
    response = stock_data('AAPL')
    APPLE_DF = stock_df(response)
    MONTHLY_CHANGE = monthly_change(APPLE_DF)
    
    # Creates a line plot
    plt.plot(MONTHLY_CHANGE)
    plt.xlabel('Months since April 2000')
    plt.ylabel('Monthly Change in Stock Price ($)')
    plt.title('Changes Stock Price Monthly from April 2000 - March 2020')
    plt.show()
    

def largest_impact():

    # Retrieves the data for Apple and reports the change in stock
    # for the month
    response = stock_data('AAPL')
    APPLE_DF = stock_df(response)

    #print(APPLE_DF.head())
    #print(APPLE_DF.tail())
    
    dates = all_dates(response)
    dates.reverse()
    
    changes = monthly_change(APPLE_DF)
    changes.reverse()
    
    scores = []
    for i in range(len(dates)):
        scores.append((dates[i], changes[i]))
               

    neg_changes = [(0,0)] * 10 
    pos_changes = [(-1000, -1000)] * 10
    
    for score in scores:
        if score[1] > 0:
            for i in range(len(pos_changes)):
                if score[1] > pos_changes[i][1]:
                    pos_changes.insert(i, score)
                    pos_changes.pop(-1)
                    break
        if score[1] < 0:
            for i in range(len(neg_changes)):
                if abs(score[1]) > abs(neg_changes[i][1]):
                    neg_changes.insert(i, score)
                    neg_changes.pop(-1)
                    break

    print(neg_changes)
    print(pos_changes)

    neg_changes += pos_changes

    with open('information.csv') as infile:
        csv_contents = csv.reader(infile, delimiter = ',')

        # Extracts the headline and abstract from the CSV file
        headlines = []
        articles = []
        
        for row in csv_contents:
            ind = row[0].index('/')
            for changes in neg_changes:
                if changes[0][5] == '0':
                    month = changes[0][6]
                else:
                    month = changes[0][5:7]
                    
                if row[0][-4:] == changes[0][:4] and row[0][:ind] == month:
                    print(row[0][-4:], ' ',row[0][:ind])
                    headlines.append(row[1])
                    articles.append(row[2])

    cats = headline_category(headlines)
    print(articles)
    #scorays = abstract_sentiment(articles, cats)
    #print(scorays)
    print(cats)
    print(len(cats))

    # Name of the categories
    cat_names = ['Product Discussion', 'Apple Performance',
                 'Apple Competitors', 'Undescriptive']
    
    cat_buckets = [0,0,0,0,0]
    
    # Adds 1 to each bucket when an aricle falls in that category
    for i in range(len(cats)):
        num = cats[i]
        cat_buckets[num - 1] += 1

    # Creates a bar graph
    pos = [i for i in range(4)]
    plt.bar(pos, cat_buckets[:4])
    plt.xticks(pos, cat_names)
    plt.ylabel('Number of Articles')
    plt.xlabel('Categories')
    plt.title('Headline Category')
    plt.show()
        
                    
    
        


def main():

    # Creates a bar chart by categorizing all the headlines
    #headline_visual()
    print('hi')

    largest_impact()

    # Creates a line plot by displaing the monthly change in stock price
    # monthly_changes()
    

main()




    
