#!/usr/bin/python3
""" product api """
from endpoints import app_views
from models.user_product import Product
from models.start import storage
from flask import jsonify, request
from utils.jwt_encoding_decoding_method import verify_jwt
import base64

@app_views.route('/new_product', strict_slashes=False, methods=['POST'])
def add_new_product():
    """ add new product to the products table """
    #jwt_token = request.cookies.get("token")
    jwt_token = request.json['token']
    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    if 'type' not in data or data['type'] != 'seller':
        return jsonify({"state": "Not Authorized"}), 401

    user_id = data['data_1']
    json_data = request.json


    if ("description" not in json_data) or (
            "price" not in json_data) or (
                    "name" not in json_data) or (
                            "amount" not in json_data) or (
                                    photo_url not in json_data) or (
                                            seller_id not in json_data):

            return jsonify({"state": "bad request"}), 403

    result = storage.get_attribute(Product, "name",json_data['name'])

    if result is not None:
        return jsonify({"state": "product already exists"}), 302


    photo_url = f"/tmp/{json_data['name'].jpg}"
    with open(photo_url, encoding='utf-8') as file:
        file.write(base64.b64decode(json_data['photo_url']))

    json_data['photo_url'] = photo_url

    new_product = Product(**json_data)

    storage.new(new_product)
    storage.save()

    return jsonify({"state": "Product is added}), 200
    

