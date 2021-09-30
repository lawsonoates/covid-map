def latest_daily_report(daily_reports):
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