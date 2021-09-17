from os import stat

from bson.objectid import ObjectId
from src.query import query_document
from bson.objectid import ObjectId

def stats_query(location):

    locs = query_document('locations', {'country_region': location})
    id = locs[0]['_id']

    reports = query_document('reports', {'location_id': id})
    report = reports[0]

    daily_report = stats_latest_daily_report(report['daily_reports'])

    stats = {
        'confirmed': daily_report['confirmed'],
        'deaths': daily_report['deaths'],
        'last_update': report['last_update']
    }
    
    return stats

def stats_latest_daily_report(daily_reports):
    '''
    Arguments:
        daily_reports (list of dictionaries) - daily reports

    Return:
        Latest daily report (dictionary)
    ''' 
    max = {'confirmed': 0, 'deaths': 0}
    for day in daily_reports:
        if day['confirmed'] > max['confirmed']:
            max = day

    return max


if __name__ == '__main__':
    print(stats_query('Australia'))