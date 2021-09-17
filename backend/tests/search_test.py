from src.search import search_query, search_iso

def test_search_query():
    result = search_query('Australia')

    assert type(result) is list

    assert result[0]['location'] == 'Australia'

def test_search_iso():
    result = search_iso('Australia')

    assert type(result) is dict

    assert result['iso'] == 'AU'