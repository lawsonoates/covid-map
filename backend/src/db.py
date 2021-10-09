import csv
import requests

from pymongo import MongoClient
from datetime import datetime

from src.tools import read_json_file, write_json_file

lookup_indexes = {}
report_indexes = {}

OWID_DUMP_PATH = './owid-covid-latest.json'
OWID_URL = 'https://covid.ourworldindata.org/data/latest/owid-covid-latest.json'
DB_URL = "mongodb://localhost:27017"

client = MongoClient(DB_URL)
covid_stats = client['covid_stats']

def get_location_collection():
    '''
    Gathers all specified data from each valid country and returns each country amongst a list of
    reports.

    Arguments:
        none

    Return:
        collection (list) - list of reports to form collection in db
    ''' 

    locations = []

    with open('lookup.csv') as file:
        file_data = csv.reader(file)

        for row in file_data:
            if not row[lookup_indexes['Province_State']] and not row[lookup_indexes['iso2']] == '':
                locations.append({
                    # 'UID': row[lookup_indexes['UID']],
                    'ISO2': row[lookup_indexes['iso2']],
                    'ISO3': row[lookup_indexes['iso3']],
                    'country_region': row[lookup_indexes['Country_Region']],
                    'population': int(row[lookup_indexes['Population']])
                })

    return locations

def get_reports_collection():
    '''
    Gathers all specified data from each valid country and returns each country amongst a list of
    reports.

    Arguments:
        none

    Return:
        reports (list) - list of reports to form collection in db
    ''' 

    reports = []

    locations = covid_stats['locations'].find()

    file_data = read_json_file(OWID_DUMP_PATH)

    i = 0
    for location in locations:

        iso3 = location['ISO3']

        owid_str = f'OWID_{iso3}'

        if iso3 in file_data.keys():
            reports.append({
                'location': file_data[iso3]['location'],

                'total_cases': file_data[iso3]['total_cases'],
                'new_cases': file_data[iso3]['new_cases'],
                'new_cases_smoothed': file_data[iso3]['new_cases_smoothed'],

                'tests_per_case': file_data[iso3]['tests_per_case'],

                'total_deaths': file_data[iso3]['total_deaths'],

                'reproduction_rate': file_data[iso3]['reproduction_rate'],

                'people_fully_vaccinated_per_hundred': file_data[iso3]['people_fully_vaccinated_per_hundred'],

                'last_update_date': file_data[iso3]['last_updated_date'],
                'location_id': location['_id']
            })

        # elif owid_str in file_data.keys():
        #     collection.append({
        #         'location': file_data[owid_str]['location'],
        #         'total_cases': file_data[owid_str]['total_cases'],
        #         'new_cases': file_data[owid_str]['new_cases'],
        #         'new_cases_smoothed': file_data[owid_str]['new_cases_smoothed'],
        #         'last_update_date': file_data[owid_str]['last_updated_date'],
        #         'location_id': location['_id']
        #     })

    return reports

def db_indexes():
    '''
    Populates data within dictionaries to be used for other functions to easily reference csv data.

    Arguments:
        none

    Return:
        none
    ''' 

    count = 0
    with open('./lookup.csv') as file:
        file_data = csv.reader(file)
        for row in file_data:
            if count < 1:
                i = 0
                for col in row:
                    lookup_indexes[col] = i
                    i += 1

            count += 1

    count = 0
    with open('./downloaded.csv') as file:
        file_data = csv.reader(file)
        for row in file_data:
            if count < 1:
                i = 0
                for col in row:
                    report_indexes[col] = i
                    i += 1

            count += 1

def db_remove_collection(collection_names):
    '''
    Removes all collections specified from db.

    Arguments:
        collection_names (list) - list of collections to be removed

    Return:
        none
    ''' 

    for name in collection_names:
        col = covid_stats[name]
        col.drop()

def db_add_docs(collection_name, docs):
    '''
    Inserts docs into specified db collection.

    Arguments:
        collection_name (str) - name of collection to add doc
        docs (list) - list of docs to add to collection

    Return:
        none
    ''' 
    collection = covid_stats[collection_name]
    collection.insert_many(docs).inserted_ids

def get_new_update():
    '''
    Creates a HTTP request to download covid data from url. Writes to file if successful and calls
    db_update().

    Arguments:
        none

    Return:
        none
    ''' 

    try:
        req = requests.get(OWID_URL)
    except requests.exceptions.ConnectionError:
        print('connection refused')

    # if ok request then write to file and update db
    if req.status_code == 200:
        write_json_file(OWID_DUMP_PATH, req.json())
        db_update()

def db_update():
    '''
    Calls functions to remove old data from db and add new data.

    Arguments:
        none

    Return:
        none
    '''

    db_indexes()

    db_remove_collection(['locations', 'reports'])

    db_add_docs('locations', get_location_collection())

    db_add_docs('reports', get_reports_collection())
    
def db_refresh():
    '''
    Is called by client refresh request and determines if new request should be made for db data.
    Criteria includes last refresh request time and date of current data.

    Arguments:
        none

    Return:
        'success' (str) - used to pass to client to confirm refresh has been attempted.
    ''' 

    today = datetime.today().strftime('%Y-%m-%d')
    hour = datetime.now().hour

    db_properties = read_json_file('./db_properties.json')

    last_update_date = db_properties['last_update_date']
    last_update_hour = db_properties['last_update_hour']

    # updates if db is not current to the day and more than 1 hour has lapsed since last call
    if last_update_date < today and last_update_hour < str(hour):
        get_new_update()
        write_json_file('./db_properties.json', {
            "last_update_date": today,
            "last_update_hour": hour
        })

    return 'success'

if __name__ == '__main__':
    get_new_update()