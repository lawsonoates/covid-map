from src.query import query_document, query_document_property, query_location_fixed

def test_query_document_exact():

    collection_name = 'locations'
    query = {'country_region': 'Australia'}

    result = query_document(collection_name, query)

    assert type(result) is list

    assert type(result[0]) is dict

    assert result[0]['country_region'] == 'Australia'

def test_query_document_inclusive():

    collection_name = 'locations'
    query = {'country_region': {'$regex': 'au', '$options': '$i'}}

    result = query_document(collection_name, query)

    assert type(result) is list

    assert type(result[0]) is dict

    found_australia = False
    found_austria = False
    for entry in result:
        if entry['country_region'] == 'Australia':
            found_australia = True
        elif entry['country_region'] == 'Austria':
            found_austria = True
        
    assert found_australia == True
    assert found_austria == True

def test_query_document_property():

    collection_name = 'locations'
    query_value = 'Australia'
    property_desired = 'ISO2'
    property_query = 'country_region'

    result = query_document_property(collection_name, query_value, property_desired, property_query)

    assert type(result) is list

    assert type(result[0]) is str

    assert result[0] == 'AU'

def test_query_location_fixed():

    location = 'Australia'

    result = query_location_fixed(location)

    assert type(result) is str

    assert result == 'AU'
