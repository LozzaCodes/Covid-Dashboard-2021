""" this module handles all retrievals
of quantitative covid data from a third
party API run by the NHS.
It also handles storage of this data
and conversions between json and csv files
"""
import csv
import json
import logging
import time
from datetime import datetime
from sched import scheduler
from requests import get
from uk_covid19 import Cov19API
import file_handler
import covid_news_handling

logging.basicConfig(filename='system.log', encoding='utf-8', level=logging.DEBUG)
configfile = file_handler.initialise_file("config.json") #initiates the config file for the module
schedule = scheduler(time.time, time.sleep)

def parse_csv_data(csv_filename): #this function takes an input csv and returns a list of contents
    """ this function opens an input filename
    and reads the contents, adding each line to a list
    of dictionaries containing data

    Arguments:
        csv_filename - string
    Parameters:
        contentslist - a list of dictionaries
    """
    contentslist = []
    counter = 0
    file = open(csv_filename, "r", encoding="utf-8") #input filename is opened with read permissions
    filecontents = csv.reader(file) #csv module is used to retrive data from the csv file
    for counter in filecontents: #iterates through each line of the csv file
        contentslist.append(counter)
    file.close()
    return contentslist

def process_covid_csv_data(covid_csv_data):
    """ this module reads an input list of data dictionaries
    and reads through it, retrieving key data values.
    Arguments:
        covid_csv_data - list of data dictionaries
    Parameters: 3 integers -
        Current hospital cases
        Current total deaths
        Recent 7 day infection rate
    """
    #calculates current hospital cases
    temp = covid_csv_data[1]
    current_hospital_cases = temp[5]
    if current_hospital_cases != "":
        current_hospital_cases = int(current_hospital_cases)
    #calculates total deaths
    searchflag, searchcounter = False, 1
    while searchflag is not True and searchcounter < 20: #iterates until data is present
        temp2 =  covid_csv_data[searchcounter]
        if temp2[4] != "":
            searchflag = True
        searchcounter += 1
    total_deaths = (covid_csv_data[searchcounter-1])[4]
    #calculates 7 day cases
    casecounter, last7days_cases  = 3, 0
    while casecounter < 10: #iterates through the csv data 7 times
        temp3 = covid_csv_data[casecounter]
        last7days_cases += int(temp3[6])
        casecounter += 1
    if total_deaths != "":
        total_deaths = int(total_deaths)
    return last7days_cases, current_hospital_cases, total_deaths

def convert_to_csv(outputfile):
    """ This module opens a json store of
    api data and opens a csv file (of the input string)
    and writes the contents of the json into the csv

    Arguments:
        outputfile - string
    """
    with open(configfile["jsonstore"], "r", encoding="utf-8") as json_file:
        apidata = (json.load(json_file))["data"]
    csvfile = open(outputfile, 'w', newline='', encoding="utf-8") #empty lines not added
    csv_writer = csv.writer(csvfile) #stores the csv.writer(csvfile) function
    count = 0
    for datarow in apidata: #iterates through apidata, writing all the keys and values to the csv.
        if count == 0:
            header = datarow.keys()
            csv_writer.writerow(header)
            count += 1 #prevents headers being written in more than once
        csv_writer.writerow(datarow.values())
    csvfile.close() #closes the csv file once the writing has been completed

def covid_API_request(location=configfile["location"], location_type=configfile["location_type"]):
    """ this module retrieves recent covid statistics
    using a covid AP. It then stores this data in two csv files.

    Arguments:
        location - string
        location_type - string
        (Defaut values stored in config file)

    No parameters, however multiple files are written with data.
    """
    ping = get("https://newsapi.org")
    if ping.status_code == 200:
        general = ['areaType='+location_type,'areaName='+location]
        standard = {"areaCode": "areaCode",
        "areaName": "areaName",
        "areaType" : "areaType",
        "date": "date",
        "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
        "hospitalCases": "hospitalCases",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate"}
        api = Cov19API(filters=general, structure=standard)
        apidata = api.get_json() #returns a json dictionary of all the retrieved data
        with open(configfile["jsonstore"], "w", encoding="utf-8") as datacache:
            json.dump(apidata, datacache) #stores information in the aforementioned file
        if location == "England": #ensures data is stored correctly
            convert_to_csv(configfile["national_csv_store"])
            logging.info("national data stored!")
        else: #if the location value is not "England," the api request is a regional value
            convert_to_csv(configfile["regional_csv_store"])
            logging.info("regional data stored!")
        logging.info("Current covid data fully retrieved!")
    elif ping.status_code == 404:
        apidata = []
        logging.warning("API request failed! API provider may be down, \
         or API key may be invalid.")
    return apidata #this return is used purely for testing

def schedule_covid_updates(update_interval, update_name):
    """ this module is implemented mostly to fulfill
    the requirements specification outlined by the client:
    it schedules an update to the covid data using
    covid_API_request

    Arguments:
        update_interval - integer
        update_name - string
        Note: update_name is not used in this module and
        more included to fulfill the requirements.
        Finding a use for it in this module could
        be an improvement for later releases of this
        software
    """
    schedule.enter(update_interval, 1, covid_API_request, ())
    schedule.enter(update_interval, 2, covid_API_request, ("England", "nation",))

def schedule_all_updates():
    """ this module will read through a list of updates stored in config.json
    and for each entry schedule an event. If an event is not a repeat event,
    it is then deleted.

    No arguments or paremeters, however part of the program's app data file
    is read from and written to
    """
    appdata = file_handler.initialise_file("appdata.json")
    count = 0
    while count < len(appdata["update_list"]):
        update_wait = 0
        current_update = appdata["update_list"][count]
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        update_time=datetime.strptime(current_update["content"], "%H:%M")
        update_time_seconds = (update_time.hour * 3600) + (update_time.minute * 60)
        current_hours = int(current_time[0] + current_time[1])
        current_minutes = int(current_time[3] + current_time[4])
        current_time_in_seconds = (current_hours* 3600) + (current_minutes * 60)
        update_wait = update_time_seconds - current_time_in_seconds
        if update_wait < 0:
            update_wait = 86400 + update_wait
        coviddata = current_update["covid_data"]
        news = current_update["news_data"]
        repeat = current_update["repeat"]
        #this segment of code schedules the actual event
        if coviddata is True:
            schedule_covid_updates(update_wait, current_update["title"])
            logging.info("covid update scheduled!")
        if news is True:
            schedule.enter(update_wait, 3, covid_news_handling.news_API_request, ())
            logging.info("news update scheduled!")
        if repeat is False:
            schedule.enter(update_wait, 4, appdata["update_list"].pop, (count,))
        count += 1
        logging.info(schedule.queue)
