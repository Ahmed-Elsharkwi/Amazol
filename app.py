#!/usr/bin/python3
""" main end point """

from flask import Flask, make_response, jsonify, request, render_template, make_response
from flask_cors import CORS
from endpoints import app_views
from models.start import storage


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.register_blueprint(app_views)


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
