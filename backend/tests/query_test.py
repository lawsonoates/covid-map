from src.query import query_document, query_location

def test_query_document_exact():

    collection_name = 'locations'
    query = {'country_region': 'Australia'}

    result = query_document(collection_name, query)

    assert type(result) is list

    assert result[0]['country_region'] == 'Australia'


def test_query_location():

    collection_name = 'locations'
    query = {'country_region': {'$regex': 'Aus', '$options': '$i'}}

    assert type(query_location(collection_name, query)) is list
