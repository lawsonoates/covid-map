from pymongo import MongoClient
from bson.objectid import ObjectId
import csv
import os

UID_INDEX = 0
ISO2_INDEX = 1
PROVINCE_STATE_INDEX = 6
COUNTRY_REGION_INDEX = 7
POPULATION_INDEX = 11

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
            if not row[PROVINCE_STATE_INDEX]:
                docs.append({
                    'UID': row[lookup_indexes['UID']],
                    'ISO2': row[lookup_indexes['iso2']],
                    'country_region': row[lookup_indexes['Country_Region']],
                    'population': row[lookup_indexes['Population']]
                })

    return docs

def get_reports_collection():
    collection = []

    # get latest report file
    folderpath = './reports'
    files = os.listdir(folderpath)

    file_count = 0
    for filename in files:
        filepath = folderpath + '/' + filename

        with open(filepath) as file:
            file_data = csv.reader(file)

            prev_value = ''
            dataset = {}
            count = 0
            for row in file_data:
                
                if count > 0:
                    # unique row
                    if not row[report_indexes['Country_Region']] == prev_value:
                        if prev_value == '':
                            dataset = {
                                'confirmed': int(row[report_indexes['Confirmed']]),
                                'deaths': int(row[report_indexes['Deaths']])
                            }
                            
                        if file_count == 0:
                            collection.append({
                            'country_region': row[report_indexes['Country_Region']],
                            'last_update': '',
                            'reports': [dataset]
                        })
                        else:
                            for report in collection:
                                if report['country_region'] == row[report_indexes['Country_Region']]:
                                    report['reports'].append(dataset)

                        dataset = {
                            'confirmed': int(row[report_indexes['Confirmed']]),
                            'deaths': int(row[report_indexes['Deaths']])
                        }
                    # not unique row
                    else:
                        dataset = {
                            'confirmed': dataset['confirmed'] + int(row[report_indexes['Confirmed']]),
                            'deaths': dataset['deaths'] + int(row[report_indexes['Deaths']])
                        }

                    prev_value = row[report_indexes['Country_Region']]

                count += 1

        file_count += 1

    return collection

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

def query_location_iso(iso):
    result = query_document('locations', {'ISO2': iso})
    return [x['country_region'] for x in result]

if __name__ == '__main__':
    get_indexes()

    # collections = match_collection_id(get_lookup_collection(), get_reports_collection())
    
    # add_docs_db('reports', collections['secondary'])
    # add_docs_db('locations', collections['primary'])

    # print(query_location_iso('AU'))