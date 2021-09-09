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

    dates = ['09-05-2021', '09-04-2021', '09-03-2021', '09-02-2021', '09-01-2021', '08-31-2021', '08-30-2021']

    for date in dates:
        req = requests.get(URL + f'/{date}.csv')

        url_content = req.content
        csv_file = open(f'./reports/{date}.csv', 'wb')

        csv_file.write(url_content)
        csv_file.close()

    return url_content

if __name__ == '__main__':
    get_data()
