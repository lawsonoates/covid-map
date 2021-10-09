import json

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

def write_json_file(url, data):
    '''
    Arguments:
        url (string) - path of json file to write to
        data (dict) - data to write

    Return:
        none
    ''' 

    with open(url, 'w') as f:
        json.dump(data, f)

def read_json_file(url):
    '''
    Arguments:
        url (string) - path of json file to read

    Return:
        data (dict) - data read from json file
    ''' 

    with open(url, 'r') as f:
        data = json.load(f)

    return data