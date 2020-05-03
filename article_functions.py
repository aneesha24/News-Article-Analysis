'''
    Aneesha Sreerama
    Alexander Deris
    DS2000
    Semester Project
'''

# Keyword Categories:

# 1. Product Releases
# 2. Coverage on Software Issues
# 3. Competitors
# 4. Types of products
# 5. Exchanges
# 6. Keywords in Press Releases
# 7. Words associated with downward Trends
# 8. Words associated with upward trends
# 9  Words that come up when Apple does not have a lot of media attention
#    (The API collects the top 10 articles that best fit the request filters.
#     Accordingly, in the months where Apple does not have major press, articles 
#     are mostly about the "Big Apple" or other events in New York)
# 10. Legal Events
# 11. CEOs of Apple


keywords = {
'releases':['unveil', 'new', 'edition', 'version', 'high-end', 'debut', 'upgrade', 'dominant',
            'prototype', 'open'],
'problems' : ['problem', 'attack', 'slow', 'block', 'technical', 'issues', 'stumble',
              'technology challenges', 'warning', 'hack', 'failure'],
'competitors' : ['microsoft', 'google', 'gateway', 'compaq', 'palm', 'blackberry', 'i.b.m', 
               'ibm', 'roxio', 'sony', 'realnetworks', 'sun microsystems', 'yahoo', 'nbc',
               'dell', 'hewlett-packard', 'htc', 'samsung', 'twitter', 'ericsson', 'zune',
               'facebook', 'nokia', 'xiamo', 'myspace'],
'product_type' : ['computer', 'laptop', 'music', 'podcast', 'TV', 'autonomous', 'pay', 'cellphone', 'os',
                 'notebook', 'watch', 'e-book', 'operating', 'system', 'desktop', 'technology', 'store'],
'exchanges' : ['nasdaq', 'dow jones' 'standard & poor\'s', 'Nasdaq', 'Dow' 'Poor\'s'],
'margins' : ['earnings', 'profit', 'income', 'stock', 'share'],                 
'down_trends' : ['loss', 'lost', 'losing', 'bearish', 'drop', 'sink', 'sunk', 'crash', 'slump', 'plunge'],
'up_trends' : ['gain', 'increase','double', 'triple', 'rise', 'rose', 'rising', 'jump',
              'bullish', 'strong', 'top', 'soar'],          
'lack' : ['Big Apple', 'New York'],
'legal' : ['sue', 'lawsuit', 'patent', 'settle', 'antitrust', 'ban', 'f.b.i', 'fbi', 'stealing'],
'ceos' : ['Steve', 'Jobs', 'jobs', 'Timothy', 'Tim', 'Cook', 'cook']}



def search_products(words):
    ''' Function: search_products
        Parameters: A list of words or a portion of a sentence (List/String)
        Returns: If an Apple Product is mentioned in the input (Boolean)
    '''

    if not(isinstance(words, list)):
        # Splits the headline into a list of Strings
        words = words.split()

    # Determines if the name of a product is in the list
    product = False
    for word in words:
        # Searches for products such as iPhone, iTunes, iCloud...
        if word[0] == 'i' and (word[1] in 'PMBCTLHWSTOM'):
            product = True

        # Searches for Apple products with the 'Mac' prefix
        elif 'mac' == word.lower()[:3]:
            product = True
            
    return product

    

def trend_score(trends):
    ''' Function: trend_score
        Parameters: Portion of a sentence (String)
        Returns: The number of words synonymous with "up" and "down"(List)
    '''

    # Counts the words assocaitd with each of these trends
    down = 0
    up = 0

    # Determines if the word falls in either one of these caegories
    for trend in trends:
        for down_trend in keywords['down_trends']:
            if down_trend in trend:
                down += 1

        for up_trend in keywords['up_trends']:
            if up_trend in trend:
                up += 1

    # Returns the number of words synonymous with "up" and "down"
    return [down, up]

def product_analysis(words, metrics):
    ''' Function: product_analysis
        Parameters: words from the abstract (List)
                    represents the types of article content (list)
        Returns: modified types of article content (list)
    '''

    
    # Determines if the article was centered around a new Apple Product
    for word in words:
        for release in keywords['releases']:
            if release in word or release in word.lower():
                index = words.index(word)
                indicators = words[index:(index + 5)]
                metrics[5] = search_products(indicators)

                if not metrics[5]: 
                    for indicator in indicators:
                        for product in keywords['product_type']:
                            if indicator == product:
                                metrics[5] = True 

    # Determines if the article was centered issues with an Apple Product
    for word in words:
        for problem in keywords['problems']:
            if problem in word or problem in word.lower():
                index = words.index(word)
                indicators = words[(index - 5):(index + 5)]
                metrics[1] = search_products(indicators)

                if 'Apple' in indicators:
                    metrics[1] == True

    if metrics[1] == False and metrics[5] == False:
        metrics[2] = search_products(words)

    return metrics

def competitor_analysis(words, metrics):
    ''' Function: competitor_analysis
        Parameters: words from the abstract (List)
                    represents the types of article content (list)
        Returns: modified types of article content (list)
    '''

    # Apple competing with Microsoft?
    for word in words:
        if 'Microsoft' == word:
            metrics[0] = True

        
    # Apple in a lawsuit or sued?
    for word in words:
        if metrics[3] == True:
            break
        for issue in keywords['legal']:
            if issue in word:
                index = words.index(word)

                for j in range(index):
                    if words[j][0] in 'ABCDEFGHIUKLMNOPQRSTUV':
                        if word in keywords['competitors']:
                            metrics[3] == True

    return metrics

def performance_analysis(words, metrics):
    ''' Function: performance_analysis
        Parameters: words from the abstract (List)
                    represents the types of article content (list)
        Returns: modified types of article content (list)
    '''

    overall = [0,0]
    # Determines how Apple performed by finding words associated
    # with gains and losses
    for word in words:
        if word in keywords['margins'] or word in keywords['exchanges']: 
            index = words.index(word)
            indicators = words[index:(index + 5)]
            score = trend_score(indicators)
            
            overall[0] += score[0]
            overall[1] += score[1]

    metrics[6] = overall[1] - overall[0]

    return metrics
    

def unrelated(metrics):
    ''' Function: performance_analysis
        Parameters: words from the abstract (List)
                    represents the types of article content (list)
        Returns: modified types of article content (list)
    '''
    
    switch = 0
    for i in range(5):
        if metrics[i] == True:
            switch = 1
    if switch == 0:
        metrics[5] = True

    return metrics

    
def abstract_sentiment(abstracts, categories):
    ''' Function: abstract_sentiment
        Parameters: List of article abstacts (List of Strings)
                    List of categorizations for news headlines (List of Numbers)
        Return: Rating for the month's worth of articles
    '''
    cates = [0, 0, 0, 0, 0, 0, 0]
    # Assigns a weight for each metric and article category 
    A_WEIGHT = [-1.75, -3.25, 0.25, -4, -0.25, 2, 3]
    H_WEIGHT = [2.5, 0.5, 3, 0.5, 0.75]

    # Stores the sentiment score for each article
    sentiment = []
    
    for i in range(len(categories)):

        metrics = [False, False, False, False, False, False, 0]


        # The abstract of the article discussed...
        # metrics[0] - Competition with Microsoft
        # metrics[1] - Any problems associated with Apple's tech
        # metrics[2] - Commentary on Apple products
        # metrics[3] - Lawsuits with other tech companies
        # metrics[4] - Something unrelated to Apple Company
        # metrics[5] - An introduction of a new Apple product
        # metrics[6] - Sales/market growth
        
        
        # Turns a String into a List of Strings
        words = abstracts[i].split()
        
        # Analyzes the text of the abstract
        metrics = competitor_analysis(words, metrics)
        metrics = product_analysis(words, metrics)
        metrics = performance_analysis(words, metrics)
        metrics = unrelated(metrics)


        for j in range(len(metrics)):
            if metrics[j] == True:
                cates[j] += 1

        #print(cates)

        
        for i in range(len(metrics)):
            if metrics[i] == True:
                metrics[i] = 1
            elif metrics[i] == False:
                metrics[i] = 0

        score = 0
        for k in range(len(metrics)):
            score += (metrics[k] * A_WEIGHT[k])
            index = categories[k] - 1
            score = score * H_WEIGHT[index]

        sentiment.append(score)
    
    return sentiment #(sum(sentiment) / 10)


def headline_category(headlines):
    ''' Function: headline_category
        Parameter: list of headlines (List of Strings)
        Returns: list of categories (List of ints)
    '''

    # Categorize by type of news
    # 1. Product Discussion
    # 2. Apple vs Competitors
    # 3. Apple/Market Performance
    # 4. Undescriptive headline
    # 5. Not related to Apple Company
    

    # List to hold the type of article based on the headline
    categories = [] 

        
    for headline in headlines:

        # Corresponds to category number
        num = 0

        # Determines if "Big Apple" or "New York" are in the headline - easiest way to determine
        # if the news is most likely NOT about Apple
        if keywords['lack'][0] in headline or keywords['lack'][1] in headline:
            num = 5

        # Determines if any Apple products are mentioned in the Headline
        # If so, the article is most likely about said product
        else:
            products = search_products(headline)
            if products == True:
                num = 1

        if num != 0:
            categories.append(num)
            
        else:

            # Keeps track of "keyword finds"
            score = 0
            
            # Splits the headline into a list of Strings
            words = headline.lower().split()
            words_length = len(words)


            # Checks whether the word is related to any word in the keywords dictionary
            for m in range(len(words)):

                # If a keyword is found the loop is terminated
                if num != 0:
                    categories.append(num)
                    break

                # Otherwise the word is searched through the keywords
                else:
                    for key in keywords.keys():
                        for i in range(len(keywords[key])):
                            if keywords[key][i] in words[m]:
                                if score == 0:
                                    score += 1 

                                    # Categorizes the article based on the keyword found
                                    if key in ['releases', 'problems', 'product_type', 'ceos']:
                                        num = 1
                                    elif key in ['competitors', 'legal']:
                                        num = 2
                                    elif key in ['margins', 'exchanges', 'down_trends', 'up_trends']:
                                        num = 3

                if m == (words_length - 1) and num != 0:
                    categories.append(num)
                                        
            # Not enough information to determine what is in the article
            if score == 0 and len(words) <= 6:
                num = 4
                categories.append(num)

            # Most likely not related to Apple Company
            elif score == 0:
                num = 5
                categories.append(num)
    
    return categories
            
def testing():

    headlines = ['Apple Reports Big Profits and 2-for-1 Split',
                 'U.S. Hoping 2 Microsoft Monopolies Are Gentler Than One',
                 'Laptops of Luxury, When Price Is an Afterthought',
                 'My Life, My Laptop',
                 'Apple to Postpone Software Upgrade',
                 'As Honeybees Bow Out, Others Join the Cast',
                 'BUSINESS DIGEST',
                 'Mixing OS X and Microsoft',
                 'Apple Is Introducing \'Future of Macintosh\'',
                 'Apple Issues Earnings Warning']

    abstracts = ['Microsoft plans new software for Apple Computer\'s Macintosh computers; photo (M)',
                 'Robert Nielsen letter comments on Sept 14 article on new Apple operating system',
                 'State of the Art column appraises Apple Computer Inc\'s new Power Mac G4 Cube computer; drawing (M)',
                 'Question and answer column on computer problems (M)',
                 'Article describes scene on distinctive red double-decker bus from New York Apple..',
                 'Apple Computer Co names Arthur D Levinson, chairman of Genentech, to its board (S)',
                 'Question and answer column on computer problems (M)',
                 'Microsoft plans new software for Apple Computer\'s Macintosh computers; photo (M)',
                 'J D Biersdorfer and Don Donofrio article of their test of beta version of Mac OS X software (M)',
                 'Profile of embattled New YoÄ']

    categories = headline_category(headlines)
    print(categories)
    print(abstract_sentiment(abstracts, categories))

#testing()
                 
                 
                 
                 
                 
                 
                 
                 


        

        

    
