# from server import stats
from pymongo import MongoClient
from bson.objectid import ObjectId
import csv
import os

from datetime import date, datetime
from src.error import InputError
# from src.stats import stats_max_daily_report


CSV_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

lookup_indexes = {}
report_indexes = {}

# Replace the uri string with your MongoDB deployment's connection string.
DB_URL = "mongodb://localhost:27017"
# set a 5-second connection timeout
client = MongoClient(DB_URL)
covid_stats = client['covid_stats']

def get_lookup_collection():
    docs = []

    with open('lookup.csv') as file:
        file_data = csv.reader(file)

        for row in file_data:
            if not row[lookup_indexes['Province_State']]:
                docs.append({
                    'UID': row[lookup_indexes['UID']],
                    'ISO2': row[lookup_indexes['iso2']],
                    'country_region': row[lookup_indexes['Country_Region']],
                    'population': row[lookup_indexes['Population']]
                })

    return docs

def get_reports_collection():
    collection = []

    folderpath = './reports'
    files = os.listdir(folderpath)

    file_count = 0
    for filename in files:
        filepath = folderpath + '/' + filename

        with open(filepath) as file:
            file_data = csv.reader(file)

            prev_value = ''
            dataset = {}
            row_count = 0

            report = {
                    'country_region': '',
                    'last_update': '',
                    'daily_reports': []
                }

            summary = {
                'country_region': '',
                'last_update': '',
                'confirmed': 0,
                'deaths': 0
            }
            

            for row in file_data:

                # neglect header row
                if row_count > 0:

                    if row[report_indexes['Country_Region']] == summary['country_region']:
                        summary['confirmed'] += int(row[report_indexes['Confirmed']])
                        summary['deaths'] += int(row[report_indexes['Deaths']])

                    else:
                        collection = db_put_into_collection(summary, collection)

                        summary = {
                            'country_region': row[report_indexes['Country_Region']],
                            'last_update': row[report_indexes['Last_Update']],
                            'confirmed': int(row[report_indexes['Confirmed']]),
                            'deaths': int(row[report_indexes['Deaths']])
                        }

                row_count += 1

        file_count += 1

    return collection

def db_put_into_collection(summary, collection):

    found = False
    for location in collection:
        if location['country_region'] == summary['country_region']:
            # location['last_update'] = get_latest_date(location['last_update'], summary['last_update'], CSV_TIME_FORMAT)
            location['daily_reports'].append({
                'confirmed': summary['confirmed'],
                'deaths': summary['deaths']
            })
            found = True

    if not found:
        collection.append({
            'country_region': summary['country_region'],
            'last_update': summary['last_update'],
            'daily_reports': [{
                'confirmed': summary['confirmed'],
                'deaths': summary['deaths']
            }]
        })

    return collection

def get_latest_date(date1, date2, format):

    date1_date = datetime.strptime(date1, format)
    date2_date = datetime.strptime(date2, format)

    # print(date1_date + ' | ' + date2_date)
    date_max = max([date1_date, date2_date])

    date_str = date_max.strftime(format)

    return date_str

def get_indexes():

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


def match_collection_id(collection_primary, collection_secondary):

    for entry_primary in collection_primary:
        temp_id = ObjectId()
        entry_primary['_id'] = temp_id
        country_region = entry_primary['country_region']
        for entry_secondary in collection_secondary:
            if entry_secondary['country_region'] == country_region:
                entry_secondary['location_id'] = temp_id

    return {
        'primary': collection_primary,
        'secondary': collection_secondary
    }


def add_docs_db(collection_name, docs):
    collection = covid_stats[collection_name]
    doc_id = collection.insert_many(docs).inserted_ids
    print(doc_id)

def query_document(collection_name, query):
    result = covid_stats[collection_name].find(query)
    return [x for x in result]

def query_location(property, country_region):
    result = query_document('locations', {'country_region': {'$regex': f'{country_region}', '$options': '$i'}})

    return [x[property] for x in result]

def query_location_fixed(location):
    result = query_document('locations', {'country_region': location})
    print(len(result) != 1)
    if len(result) != 1:
        raise InputError('invalid location input')
    else:
        return result[0]['ISO2']

def query_location_iso(iso):
    result = query_document('locations', {'ISO2': iso})
    return [x['country_region'] for x in result]

def stats_max_daily_report(daily_reports):
    
    max = {'confirmed': 0, 'deaths': 0}
    for day in daily_reports['reports']:
        if day['confirmed'] > max['confirmed']:
            max = day

    return max

def insert_analysis():

    reports = list(covid_stats['reports'].find())
    for report in reports:
        if report['country_region'] == 'Australia':
            daily_reports = stats_max_daily_report(report['daily_reports'])
            population = query_document('locations', {'_id': report['location_id']})
            return population
            # report['incident_rate'] = 

    return reports

def db_update(status):
    get_indexes()
    collections = match_collection_id(get_lookup_collection(), get_reports_collection())

    # print(collections)

    if status == 'all':
        add_docs_db('reports', collections['secondary'])
        add_docs_db('locations', collections['primary'])
    elif status == 'r':
        add_docs_db('reports', collections['secondary'])

if __name__ == '__main__':
    get_indexes()

    
    
    # print(get_reports_collection())

    # print(query_location_iso('AU'))
    # print(query_location_fixed('Australia'))
    # print(get_lookup_collection())
    # data = insert_analysis()
    # print(data)

    collection1 = [{
        'UID': '36',
        'ISO2': 'AU',
        'country_region': 'Australia',
        'population': '25459700'
    }]

    collection2 = [{
        'country_region': 'Australia',
        'last_update': '2021-09-03 04:21:20',
        'daily_reports': [
            { 'confirmed': 58208, 'deaths': 1032 },
            { 'confirmed': 55093, 'deaths': 1012 },
            { 'confirmed': 61619, 'deaths': 1039 },
            { 'confirmed': 59949, 'deaths': 1036 },
            { 'confirmed': 56560, 'deaths': 1019 },
            { 'confirmed': 64621, 'deaths': 1052 },
            { 'confirmed': 63155, 'deaths': 1044 }
        ]
    }]

    # print(match_collection_id(collection1, collection2))
    db_update('all')