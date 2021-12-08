""" this module handles the retrieval
of recent news data using a third party News API.
It also handles the creation of a list of five
relevant articles for the user - excluding ones
the user has previously deleted
"""
import logging
from newsapi.newsapi_client import NewsApiClient
import file_handler

logging.basicConfig(filename='system.log', encoding='utf-8', level=logging.DEBUG)
configfile = file_handler.initialise_file("config.json") #initiates the config file for the module
appdata = file_handler.initialise_file("appdata.json")

def news_API_request(covid_terms="Covid COVID-19 coronavirus"): #returns dictionary of articles
    """ this module uses the News Api Client to
    retrieve news articles that contain the requested keywords.

    Arguments:
        covid_terms - string (standard value = "Covid COVID-19 coronavirus")
    Parameters:
        top_articles - dictionary
    """
    covid_terms = covid_terms.replace(" ", " OR ") #formats the query
    if configfile["api_key"] == "":
        logging.warning("There is no API key provided - please add an API key to the config file.")
        top_articles = []
    else:
        newsapi = NewsApiClient(api_key=configfile["api_key"]) #creates a method for the news api
        top_articles = newsapi.get_everything(qintitle=covid_terms,
        language=configfile["language"],
        sort_by="relevancy")
    return top_articles

def update_news():
    """ this module compares a list of API articles
    against a list of "read" articles to return a list
    of five articles, each article formatted as a dictionary of key data

    No formal parameters, but newsarticles is appended to the config file
    """
    updated_appdata = file_handler.initialise_file("appdata.json")
    newsarticles = [] #creates an empty list to store the newsarticles which will be displayed
    readarticles =  updated_appdata["read_articles"] #retrieves a list of "read" headlines
    rawdata = news_API_request() #uses news_API_request module to retrieve data
    if rawdata["totalResults"] == 0: #in case the search retrieves no data
        logging.warning("No relevant articles found.")
    else:
        count = 0 #sets the incrementer variable initially to zero
        while len(newsarticles) < 5: #run until the number of news articles is 5
            if not rawdata["articles"][count]["title"] in readarticles:
                tempdict = {"title": "", "content": ""} #creates a temporary dictionary
                tempdict["title"] = rawdata["articles"][count]["title"]
                urltag = rawdata["articles"][count]["url"]
                urlembed = '<a href= "' + urltag + '"> Click here! </a>'
                tempdict["content"] = urlembed
                newsarticles.append(tempdict) #adds dictionary to list
            count += 1 #increments counter
    updated_appdata["unread_articles"] = newsarticles
    logging.info("News Retrieved!")
    file_handler.update_file(updated_appdata)
