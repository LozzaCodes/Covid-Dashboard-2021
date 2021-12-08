from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import schedule_covid_updates
from covid_news_handling import update_news
from covid_news_handling import news_API_request
from file_handler import initialise_file
from main import update_schedules
from main import retrieve_covid_data

def test_parse_csv_data():
    """tests parse_csv_data()"""
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request():
    data = covid_API_request()
    assert isinstance(data, dict)

def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name='update test')

def test_news_API_request():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()

def test_update_news():
    update_news()

def test_update_schedules():
    data = update_schedules()
    assert isinstance(data, list)

def test_retrieve_covid_data():
    regional_7_days, national_7_days, hospital_cases, death_total = retrieve_covid_data()
    assert isinstance(regional_7_days, int)
    assert isinstance(national_7_days, int)
    assert isinstance(hospital_cases, int)
    assert isinstance(death_total, int)

def test_initialise_file():
    data = initialise_file("testjson.json")
    assert isinstance(data, dict)

test_parse_csv_data()
test_process_covid_csv_data()
test_covid_API_request()
test_schedule_covid_updates()
test_news_API_request()
test_update_news()
test_update_schedules()
test_retrieve_covid_data()
test_initialise_file()