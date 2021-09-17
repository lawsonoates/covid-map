from flask import Flask, json, jsonify, request
from flask_cors import CORS

from src.covid_analysis import get_country_region, get_series, get_sum
from src.db import query_location, query_location_iso, query_location_fixed
from src.search import search_query, search_iso, search_location
from src.stats import stats_query

APP = Flask(__name__)
CORS(APP)

@APP.route('/stats', methods=['POST'])
def stats():
    payload = request.get_json()
    print(payload)
    location = payload['location']
    resp = stats_query(location)

    return jsonify(resp)

    # country_region = get_country_region(code)
    # data = {
    #     'region': country_region,
    #     'deaths': get_sum(get_series(country_region, 'Deaths')),
    #     'confirmed': get_sum(get_series(country_region, 'Confirmed'))
    # }
    # return jsonify(data)

@APP.route('/update_location', methods=['POST'])
def update_location():
    payload = request.get_json()
    iso = payload['iso'].upper()
    location = query_location_iso(iso)

    return jsonify({'location': location})

@APP.route('/update_iso', methods=['POST'])
def update_iso():
    payload = request.get_json()
    # print(payload)
    resp = search_iso(payload['location'])
    # print(resp)
    return jsonify(resp)

@APP.route('/search/query', methods=['POST'])
def search():
    payload = request.get_json()
    resp = search_query(payload['query'])

    return jsonify(resp)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=4000)