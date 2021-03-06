from src.db import covid_stats
from src.error import InputError

def query_document(collection_name, query):
    '''
    Arguments:
        collection_name (string) - name of collection to query
        query (string) - formatted query to perform

    Return:
        result of query (list)
    ''' 
    result = covid_stats[collection_name].find(query)
    return list(result)

def query_document_property(collection_name, query_value, property_desired, property_query):
    '''
    Arguments:
        collection_name (string) - name of collection to query
        query_value (string) - value of query
        property_desired (string) - property to be returned from document
        property_query (string) - property to be used to query

    Return:
        result of query (list)
    ''' 
    result = query_document(collection_name, {property_query: {'$regex': f'{query_value}', '$options': '$i'}})

    return [x[property_desired] for x in result]

def query_location_fixed(location):
    '''
    Arguments:
        location (string) - exact name of location / country / region

    Return:
        ISO2 (string)
    ''' 
    result = query_document('locations', {'country_region': location})

    if len(result) != 1:
        raise InputError('invalid location input')
    else:
        return result[0]['ISO2']