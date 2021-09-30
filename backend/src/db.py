from pymongo import MongoClient
from bson.objectid import ObjectId
import csv
import os

from datetime import datetime
from src.error import InputError

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
            if not row[lookup_indexes['Province_State']] and not row[lookup_indexes['iso2']] == '':
                docs.append({
                    'UID': row[lookup_indexes['UID']],
                    'ISO2': row[lookup_indexes['iso2']],
                    'country_region': row[lookup_indexes['Country_Region']],
                    'population': int(row[lookup_indexes['Population']])
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
            location['last_update'] = db_latest_date(location['last_update'], summary['last_update'], CSV_TIME_FORMAT)
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

def db_latest_date(date1, date2, format):

    if date1 == '':
        return date2
    elif date2 == '':
        return date1
    else:
        date1_date = datetime.strptime(date1, format)
        date2_date = datetime.strptime(date2, format)

        date_max = max([date1_date, date2_date])

        date_str = date_max.strftime(format)

        return date_str

def db_indexes():

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
            
    # dont include reports that dont have lookup associated
    for entry_secondary in collection_secondary:
        if not 'location_id' in entry_secondary.keys():
            collection_secondary.remove(entry_secondary)

            

    return {
        'primary': collection_primary,
        'secondary': collection_secondary
    }

def db_remove_collection(collection_names):
    for name in collection_names:
        col = covid_stats[name]
        col.drop()

def db_add_docs(collection_name, docs):
    collection = covid_stats[collection_name]
    doc_id = collection.insert_many(docs).inserted_ids
    print(doc_id)

def stats_max_daily_report(daily_reports):
    
    max = {'confirmed': 0, 'deaths': 0}
    for day in daily_reports['reports']:
        if day['confirmed'] > max['confirmed']:
            max = day

    return max

def db_update(status):
    db_indexes()
    collections = match_collection_id(get_lookup_collection(), get_reports_collection())

    db_remove_collection(['reports', 'locations'])

    if status == 'all':
        db_add_docs('reports', collections['secondary'])
        db_add_docs('locations', collections['primary'])
    elif status == 'r':
        db_add_docs('reports', collections['secondary'])

if __name__ == '__main__':
    db_indexes()

    db_update('all')