from os import stat

from bson.objectid import ObjectId
from src.db import query_document
from bson.objectid import ObjectId

def stats_query(location):

    locs = query_document('locations', {'country_region': location})
    # print(locs)
    id = locs[0]['_id']
    print(id)
    o_id = ObjectId(id)


    reports = query_document('reports', {'location_id': id})
    report = reports[0]

    # # get latest day
    # max = {'confirmed': 0, 'deaths': 0}
    # for day in report['reports']:
    #     if day['confirmed'] > max['confirmed']:
    #         max = day
    
    
    return stats_max_daily_report(report)

def stats_max_daily_report(daily_reports):
    
    print(daily_reports)
    max = {'confirmed': 0, 'deaths': 0}
    for day in daily_reports['daily_reports']:
        if day['confirmed'] > max['confirmed']:
            max = day

    return max


if __name__ == '__main__':
    print(stats_query('Australia'))