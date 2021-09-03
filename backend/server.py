from flask import Flask, json, jsonify, request, send_file
from flask_cors import CORS
from json import dumps

from covid_analysis import get_country_region, get_series, get_sum, search_series

APP = Flask(__name__)
CORS(APP)

@APP.route('/stats', methods=['POST'])
def stats():
    payload = request.get_json()
    code = payload['code'].upper()

    country_region = get_country_region(code)
    data = {
        'region': country_region,
        'deaths': get_sum(get_series(country_region, 'Deaths')),
        'confirmed': get_sum(get_series(country_region, 'Confirmed'))
    }
    return jsonify(data)

@APP.route('/search', methods=['POST'])
def search():
    payload = request.get_json()
    query = payload['query']
    regions = search_series(query)
    data = []
    for i in range(0,len(regions)):
        data.append({'id': i, 'value': regions[i]})
    return jsonify(data)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=4000)