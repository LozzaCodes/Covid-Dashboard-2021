""" this is the main code for the project.
It stores all of the flask code and loads every module
This acts as the executable for the whole program
"""
import logging
from werkzeug.utils import redirect
from flask import Flask, Markup, render_template, request as flask_request
import covid_data_handler
import covid_news_handling
import file_handler

app = Flask(__name__, template_folder="templates")

#imported functions from modules are converted to variables for legibility
api_request = covid_data_handler.covid_API_request
convert_to_csv = covid_data_handler.convert_to_csv
process_data = covid_data_handler.process_covid_csv_data
parse_data = covid_data_handler.parse_csv_data
schedule_all = covid_data_handler.schedule_all_updates
update_news = covid_news_handling.update_news
configfile = file_handler.initialise_file("config.json")
appdata = file_handler.initialise_file("appdata.json")
updated_appdata = {}
update_file = file_handler.update_file
logging.basicConfig(filename='system.log', encoding='utf-8', level=logging.DEBUG)

def retrieve_covid_data():
    """ this module will gather data from csv files
    in the project directory and sift through this data to retrieve
    key values. Uses parse_data, process_data
    Parameters:
        regionaldata[2] - integer (regional seven day infection rate)
        nationalhospital - integer (national total number of hospital cases)
        ntotaldeaths - integer (national total number of deaths)
        ncaseslast7days - integer (national 7 day infection rate)
    """
    regionaldata = process_data(parse_data(configfile["regional_csv_store"]))
    nfile = configfile["national_csv_store"]
    ncaseslast7days, nationalhospital, ntotaldeaths = process_data(parse_data(nfile))
    return regionaldata[0], nationalhospital, ntotaldeaths, ncaseslast7days

def update_schedules():
    """ this function will read the list of updates stored
    in an app data file and create a list composed only of key data.

    Parameters:
        formatted_list - list of dictionaries (formatted with keys: "title" and "key")
    """
    scheduled_updates = appdata["update_list"]
    formatted_list = []
    for tempindex in scheduled_updates:
        tempdict = {"title": "", "content": ""}
        tempdict["title"] = tempindex["title"]
        tempdict["content"] = tempindex["content"]
        formatted_list.append(tempdict)
    return formatted_list

def embed_links(appdict):
    """ this module retrieves the unread_articles list
    from the appropriate appdata file (initial or updated) lists
    and converts each url string to a clickable url,
    returning each one to the correct file list.

    Parameters:
        appdict - dictionary
    """
    if len(appdict["unread_articles"]) == 0:
        pass
    else:
        listindex = 0
        for count in appdict["unread_articles"]:
            appdict["unread_articles"][listindex]["content"] = Markup(count["content"])
            listindex += 1
    logging.info("Hyperlinks added")

@app.route('/index')
def index():
    """ this function handles all the instances
    where the user has made a request in the html file.

    Arguments:
        flask_request.args - dictionary
    Parameters:
        A web page template displaying any new information requested
    """
    logging.info("User made a request!")
    if 'notif' in flask_request.args: #delete a news article
        readheadline = flask_request.args["notif"]
        templist = list(appdata["read_articles"])
        templist.append(readheadline)
        appdata["read_articles"] = templist
        #search for the news article and remove it
        articlefound = False
        count = 0
        while articlefound is False:
            if appdata["unread_articles"][count]["title"] == readheadline:
                appdata["unread_articles"].pop(count)
                articlefound = True
            count += 1
        file_handler.update_file(appdata)
    elif "update_item" in flask_request.args: #deletes an update
        targetupdate = flask_request.args["update_item"]
        templist = appdata["update_list"]
        updatefound = False
        counter = 0
        while updatefound is False and counter < len(templist):
            if templist[counter]["title"] == targetupdate:
                updatefound = True
            counter += 1
        templist.pop(counter-1)
        appdata["update_list"] = templist
        update_file(appdata)
        return redirect ("/index")
    elif 'update' in flask_request.args and not "update_item" in flask_request.args:
        #^^^ handles when a user schedules an update
        repeat_value = False
        covid_data = False
        news_data = False
        update_time = flask_request.args["update"]
        update_name = flask_request.args["two"]
        if "repeat" in flask_request.args:
            repeat_value = True
        if "covid-data" in flask_request.args:
            covid_data = True
        if "news" in flask_request.args:
            news_data = True
        #adds the update to the updatelist of config
        templist = appdata["update_list"]
        tempdict = {"title": "", "content": ""}
        tempdict["title"] = update_name
        tempdict["content"] = update_time
        tempdict["repeat"] = repeat_value
        tempdict["covid_data"] = covid_data
        tempdict["news_data"] = news_data
        templist.append(tempdict)
        appdata["update_list"] = templist
        update_file(appdata)
        return redirect ("/index")
    schedule_all()
    schedule = covid_data_handler.schedule
    schedule.run(blocking=False)
    updated_appdata = file_handler.initialise_file("appdata.json")
    r7d, nhc, ntd, n7d = retrieve_covid_data()
    embed_links(updated_appdata)
    return render_template('index.html',
        updates = update_schedules(),
        news_articles = updated_appdata["unread_articles"],
        title = "Covid-19 Dashboard",
        location = configfile["location"],
        local_7day_infections = r7d,
        nation_location = "England",
        national_7day_infections = n7d,
        hospital_cases = "Nationwide Hospital Cases: " + str(nhc),
        deaths_total = "Nationwide Deaths: " + str(ntd),
        image = configfile["image"])
@app.route("/")
def main():
    """ this function is executed at the initial
    loading of the index file. Retrieves info stored
    in the project directory regarding covid
    (this may or may not be up to date)

    Parameters:
        A web page template with integrated covid data
    """
    logging.info("Web Page opened!")
    schedule_all()
    schedule = covid_data_handler.schedule
    schedule.run(blocking=False)
    #api_request()
    #api_request("England", "nation")
    #update_news()
    embed_links(appdata)
    r7d, nhc, ntd, n7d = retrieve_covid_data()
    return render_template('index.html',
        updates = update_schedules(),
        news_articles = appdata["unread_articles"],
        title = "Covid-19 Dashboard",
        location = configfile["location"],
        local_7day_infections = r7d,
        nation_location = "England",
        national_7day_infections = n7d,
        hospital_cases = "Nationwide Hospital Cases: " + str(nhc),
        deaths_total = "Nationwide Deaths: " + str(ntd),
        image = configfile["image"])
app.run()
