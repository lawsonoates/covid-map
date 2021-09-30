
from src.db import covid_stats
from src.update import update_document_property
from src.query import query_document
from src.tools import latest_daily_report

ISO2_INDEX = 1
COUNTRY_REGION_INDEX = 7

def analyse_all():

    analyse_incident_rate()
    analyse_case_fatality_ratio()

def analyse_incident_rate():

    locations = covid_stats['locations']

    for loc in locations.find():
        query = {'location_id': loc['_id']}
        population = loc['population']

        reports = query_document('reports', query)

        if reports == []:
            print(loc)
        else:
            report = reports[0]
            daily_report = latest_daily_report(report['daily_reports'])
            cases = daily_report['confirmed']

            i_r = str(round((cases / population) * 100, 2))
            update_document_property('reports', query, {'incident_rate': i_r})     

def analyse_case_fatality_ratio():

    locations = covid_stats['locations']

    for loc in locations.find():
        query = {'location_id': loc['_id']}

        reports = query_document('reports', query)

        if reports == []:
            print(loc)
        else:
            report = reports[0]
            daily_report = latest_daily_report(report['daily_reports'])
            deaths = daily_report['deaths']
            cases = daily_report['confirmed']

            c_f_r = str(round((deaths / cases) * 100, 2))
            update_document_property('reports', query, {'case_fatality_ratio': c_f_r})  

if __name__ == '__main__':
    analyse_all()