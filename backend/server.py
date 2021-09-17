from flask import Flask, jsonify, request
from flask_cors import CORS

from src.query import query_document_property
from src.search import search_query, search_iso
from src.stats import stats_query

APP = Flask(__name__)
CORS(APP)

@APP.route('/stats', methods=['POST'])
def stats():
    payload = request.get_json()

    location = payload['location']
    resp = stats_query(location)

    return jsonify(resp)

@APP.route('/update_location', methods=['POST'])
def update_location():
    payload = request.get_json()
    iso = payload['iso'].upper()
    
    location = query_document_property('locations', iso, 'country_region', 'ISO2')

    return jsonify({'location': location})

@APP.route('/update_iso', methods=['POST'])
def update_iso():
    payload = request.get_json()

    resp = search_iso(payload['location'])

    return jsonify(resp)

@APP.route('/search/query', methods=['POST'])
def search():
    payload = request.get_json()
    resp = search_query(payload['query'])

    return jsonify(resp)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=4000)