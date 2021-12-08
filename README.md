
1. [Project Status](#project-status)
2. [Introduction](#introduction)
3. [Required Modules](#required-modules)
4. [Using the Program](#using-the-program)
5. [Interacting with the Config File](#interacting-with-the-config-file)
6. [Editing the Program](#editing-the-program)
7. [Potential Improvements](#potential-improvements)
8. [Details](#details)

## Project Status

This project is currently version 1, the first functioning release. It has not been improved by external programmers other than myself just yet, but fully tested and documented. By "fully tested" I mean I have carried out unit tests on all the functions that can be unit tested using python, and several functional tests where I executed the program and tested each function in a simulation of real-life use.  

## Introduction

This python project handles the execution, maintenance and storage of a Covid Dashboard, hosted as a html web page. The project uses several verified third party apis and standard modules in order to deliver up to date data concerning the ongoing coronavirus pandemic. This code can be used to gather information such as the local infection rate in the last seven days or the total number of deaths nationwide in order to retrieve relevant and recent news articles regarding Covid-19 and to schedule precise updates to the information provided by the dashboard. The use of a config file means the code is easily personalised and can be adapted for users all over the nation. 

## Required Modules

In order to run this project, you will have to download the following modules into your IDE:
flask,
sched,
ukcovid19,
newsapi-python.

Other modules imported in code should be standard modules built into your IDE already:
time, 
datetime, 
json, 
csv, 
logging, 
werkzeug.utils.

## Project Structure

This project was developed using a modularised workflow - code is restricted to specific functions and functions of a shared purpose/nature are assigned to modules. The full code is composed of 4 main modules: "main.py", "covid_data_handler.py", "covid_news_handling.py" and "file_handler.py." There is an additional module called "testmodules.py" which is not necessary for the program's execution, only for testing. The code that should be executed for the program to run is **"main.py".** Other files in the firectory such as "apidata.json", "appdata.json", "config.json" and the csv files "national_data.csv" and "regional_data.csv" are not executable code and act as storage for the data handled by the project. Their names can be configured using the config file (this will be explained further in the README). 

In order to open the dashboard, run main.py. The port should be hosted on http://127.0.0.1:5000/, if not this information will be accessible from system.log (the continuous log created by the program.) Type the port address into your default browser and the web page should open. Do not have any of the csv files open during operation **as this can lock the files and mean the code cannot access them.**

Do not rearrange the file structure of templates and static as these folders are essential for the operation of the module flask. If you wish to edit the website html code, go to index.html stored in the templates folder and edit it from there. 

## Using the Program

The program will open a htmp webpage and continue to run this webpage, scheduling any pre-existing updates to data displayed and refreshing every 30 seconds. As a user, you can click links to open news articles, delete news articles (these articles will not appear again after the next update of news articles) and scheduled updates and schedule updates yourself. This scheduling is done using a text box at the bottom of the page, just above several tick boxes and an entry button. Simply enter your preferred time for date of update, and tick boxes relevant to the update would like (an update of covid data, an update of news articles, whether the update will repeat). Then submit your update, and it should appear on the left side of the webpage. 

The web page can be easily edited by the developer, either using the raw html code in index.html or using the config file (see Interacting with the Config File). Monitoring the operations of the app can be done using the log file, system.log. This records every request, error and successful schedule of an event. Feel free to clear the system log if it gets too large - this might happen if you intend to use the dashboard for extended periods of time and monitor the log. 

## Interacting with the Config File

The config file of this project is an external json file to the main code that includes personal information relevant to the user, stored so that data can be extracted from the file to the code without it being an integral part of the code. This data includes a client's location, the names of local filenames and **most importantly the API key.** The API key is a key produced by News API Client for each of its users so that a user can interact with the API. You can retrieve a key for yourself by signing up for free at https://newsapi.org/. Once you have this key, copy it into the "api_key" field of the config file. This will allow data retrieval. **The code will not execute properly if you do not do this.**

Feel free to customise the contents of the config file to your heart's content - just make sure to create a backup in case the config file loses its formatting. Note: if you change the name of the image, you will also have to change the actual image file stored in static/images. 

## Editing the Program

This code is as modularised as I could make it and fully commented with both doc strings and comments in order to make the code as understandable as possible. The functionality is split between modules, with covid_data_handler controlling event scheduling and quantitative covid data retrievals, covid_news_handling controlling qualitative covid data, file_handler controlling file reading and updating, test_modules handling unit testing and main handling the data of all these functions and displaying it using flask. New modules can be added easily and one module can be adjusted without requiring all the others being changed too, but be cautious.   

## Potential Improvements

When a scheduled update is deleted, the event will still occur if the user leaves the program running until the update time. This feature does not greatly inhibit the user's experience, but could be removed in future versions. 

Due to the requirements specification given by my client, I had to move event scheduling to covid_data_handler even though this is questionable design - scheduling is not essentially part of the quantitative data retrieval category. It might make more sense to move the scheduling functions to main in future implementations, as this removes the need for a global "schedule" variable which is not very good practice.

A feature that could be useful in further implementations is a more attractive GUI that fits a range of users, one with less use of negative space and more appealing formatting and layout. This would make the dashboard seem more professional to the average end-user, hopefully improving the end user's experience. 


## Details

Developed by Laurie Harbord
Open-Source Software
Made on Windows using Visual Code

08/12/2021