from flask import Flask, jsonify, request
from flask_cors import CORS

from covid_analysis import get_country_region, get_series, get_sum
from db import query_location, query_location_iso

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

@APP.route('/iso_location_name', methods=['POST'])
def iso_location_name():
    payload = request.get_json()
    iso = payload['iso'].upper()
    location = query_location_iso(iso)

    return jsonify({'location': location})

@APP.route('/search', methods=['POST'])
def search():
    payload = request.get_json()
    query = payload['query']
    result = query_location('country_region', query)
    resp = []
    for count, value in enumerate(result):
        resp.append({'location': value})

    return jsonify(resp)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=4000)