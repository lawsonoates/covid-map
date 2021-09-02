import json
import requests

URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

def region_search(code):
    f = open('region_codes.json', 'r')
    data = json.load(f)

    for entry in data:
        if entry['Code'] == code:
            return entry['Name']

def get_data():

    req = requests.get(URL + '/08-31-2021.csv')

    url_content = req.content
    csv_file = open('downloaded.csv', 'wb')

    csv_file.write(url_content)
    csv_file.close()

    return url_content
