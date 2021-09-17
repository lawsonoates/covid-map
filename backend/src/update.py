import json
import requests
import os

from datetime import date, datetime, time, timedelta

from src.db import db_update

URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

def time_trigger():

    times = ['06:00:00', '12:00:00', '18:00:00']

    now = datetime.now()
    now_str = now.strftime('%H:%M:%S')

    if now_str in times:
        return True
    else:
        return False

def monitor():

    files = os.listdir('./reports')

    dates = []
    for file in files:
        dates.append(datetime.strptime(file, '%m-%d-%Y.csv'))

    date_max = max(dates)

    # dat = date.fromisoformat('2021-09-09')

    date_next = date_max + timedelta(days=1)
    # date_next = dat + timedelta(days=1)
    print(date_next)
    date_next_file = date_next.strftime('%m-%d-%Y.csv')

    try:
        req = requests.get(URL + date_next_file)
    except requests.exceptions.ConnectionError:
        print('connection refused')

    # ok request
    if req.status_code == 200:
        add_report(date_next_file, req)
        # db_update('r')

        # remove folder contents
        for file in files:
            os.remove('./reports/' + file)

        # add reports with decreasing datetime
        for i in range(1, 7):
            date_incr = date_next - timedelta(days=i)
            print(date_incr)
            date_incr_file = date_incr.strftime('%m-%d-%Y.csv')
            req = requests.get(URL + date_incr_file)
            add_report(date_incr_file, req)

        db_update('all')

    # error
    else:
        print('error when fetching')

def add_report(file, req):

    content = req.content
    csv_file = open('./reports/' + file, 'wb')
    csv_file.write(content)
    csv_file.close()

def region_search(code):
    f = open('region_codes.json', 'r')
    data = json.load(f)

    for entry in data:
        if entry['Code'] == code:
            return entry['Name']

if __name__ == '__main__':
    # get_data()
    monitor()
    # db_update('r')
    

