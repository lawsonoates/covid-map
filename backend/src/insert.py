from src.query import query_document
from src.db import covid_stats
from src.stats import stats_latest_daily_report

def insert_analysis():

    reports = list(covid_stats['reports'].find())
    for report in reports:
        if report['country_region'] == 'Australia':
            daily_reports = stats_latest_daily_report(report['daily_reports'])
            population = query_document('locations', {'_id': report['location_id']})
            return population
            # report['incident_rate'] = 

    return reports

# def insert_document_property(collection_name, query_value, property_desired, property_query):


