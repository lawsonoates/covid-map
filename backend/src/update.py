from src.db import covid_stats

# def update_document_property(collection_name, query_value, update_property, new_values):

#     col = covid_stats[collection_name]
#     col.update_many({update_property: {'$regex': query_value}}, {'$set': new_values})

def update_document_property(collection_name, query, new_values):

    col = covid_stats[collection_name]
    col.update_many(query, {'$set': new_values})

# if __name__ == '__main__':
#     update_document_property('reports', 'Australia', 'country_region', {'name': 'aussi'})
#     update_document_property('reports', 'Australia', 'country_region', {'name': 'aussi'})