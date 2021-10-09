from src.query import query_document

def stats_query(location):

    locs = query_document('locations', {'country_region': location})
    id = locs[0]['_id']

    reports = query_document('reports', {'location_id': id})
    report = reports[0]

    stats = {
        'total_cases': report['total_cases'],
        'new_cases_smoothed': report['new_cases_smoothed'],
        'total_deaths': report['total_deaths'],
        'last_update_date': report['last_update_date'],
        'reproduction_rate': report['reproduction_rate'],
        'people_fully_vaccinated_per_hundred': report['people_fully_vaccinated_per_hundred'],
        'tests_per_case': report['tests_per_case']
        # 'case_fatality_ratio': report['case_fatality_ratio']
    }
    
    return stats