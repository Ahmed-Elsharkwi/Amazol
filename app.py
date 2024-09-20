#!/usr/bin/python3
""" main end point """

from flask import Flask, make_response, jsonify, request, render_template, make_response
from flask_cors import CORS
from endpoints import app_views
from models.start import storage
import re


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.register_blueprint(app_views)


@app.route('/products_data/', defaults={'word': None}, methods=['POST'], strict_slashes=False)
@app.route('/products_data/<word>', methods=['POST'], strict_slashes=False)
def get_requeired_data(word):
    """ get the required data depending on the search parmeters """
    if "page" not in request.json:
        page = 1
    else:
        page = str(request.json['page'])
        res = re.match(r'^\d+$', page)
        if res is None:
            return jsonify({'state': 'Not a valid input'}), 400

    amount = 6
    offset = (int(page) * amount) - amount
    pages = False

    if 'pages' in request.json:
        pages = True

    if word is None:
        data = storage.get_products_with_offest_limit(offset, amount, pages)

    if word is not None:
        result = re.match(r'^\b([A-Za-z0-9]+(?:\s+[A-Za-z0-9]+)*)\b$', word)
        print(result)
        if result is None:
            return jsonify("Not a Valid input"), 400

        data = storage.get_products_with_offest_limit(offset, amount, pages, word)
        if "pages" not in request.json:
            pages = round(data['length'] / amount)
            data['pages'] = pages
            del data['length']
        else:
            data['pages'] = request.json['pages']

        data['page'] = page

    if len(data) == 2 or len(data) == 0:
        return jsonify("we don't have that product now"), 404

    return jsonify(data), 200


@app.teardown_appcontext
def teardown(exc):
    """ hanle teardown_qppcontext """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ handler for 404 errors """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
