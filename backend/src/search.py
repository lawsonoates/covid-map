from src.query import query_location_fixed, query_document_property
from src.error import InputError

def search_query(query):
    '''
    Arguments:
        query (string) - query of search

    Return:
        List of dictionaries of locations
    ''' 
    # locations = query_location('country_region', query)
    locations = query_document_property('locations', query, 'country_region', 'country_region')
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