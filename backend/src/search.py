from src.db import query_location, query_location_fixed
from src.error import InputError

def search_query(query):
    '''
    Arguments:
        query (string) - query of search

    Return:
        List of dictionaries of locations
    ''' 
    locations = query_location('country_region', query)
    locations_formatted = []
    for count, value in enumerate(locations):
        locations_formatted.append({'location': value})

    return locations_formatted

def search_iso(location):
    '''
    Arguements:
        location (string) - location name

    Return:
        Dictionary of iso
    '''
    
    iso = query_location_fixed(location)


    return {'iso': iso}

def search_location(iso):


    return ''

if __name__ == '__main__':
    print(search_iso('US'))