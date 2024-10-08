#!/usr/bin/python3
""" product api """
from endpoints import app_views
from models.user_product import Product, User_Product
from models.start import storage
from flask import jsonify, request
from utils.jwt_encoding_decoding_method import verify_jwt
import pybase64
import os

@app_views.route('/new_product', strict_slashes=False, methods=['POST'])
def add_new_product():
    """ add new product to the products table """
    jwt_token = request.cookies.get("seller_token")
    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    if 'type' not in data or data['type'] != 'seller':
        return jsonify({"state": "Not Authorized"}), 403

    seller_id = data['data_1']
    json_data = request.json


    if ("description" not in json_data) or (
            "price" not in json_data) or (
                    "name" not in json_data) or (
                            "amount" not in json_data) or (
                                    'photo' not in json_data):

            return jsonify({"state": "bad request"}), 400

    result = storage.get_with_one_attribute(Product, "name",json_data['name'])

    if result is not None:
        return jsonify({"state": "name already exists"}), 200

    if int(json_data['price']) <= 0 or int(json_data['amount']) <= 0:
        return jsonify({'state': "price and amount can not be 0 or less"}), 400

    photo_url = f"/static/{json_data['name']}.jpeg"
    with open(f'.{photo_url}', 'wb') as file:
        file.write(pybase64.b64decode(json_data['photo']))

    json_data['photo_url'] = photo_url
    json_data['seller_id'] = seller_id

    new_product = Product(**json_data)

    storage.new(new_product)
    storage.save()

    return jsonify({"state": "Product is added", "product_id": new_product.id}), 200
    

@app_views.route('/new_product_info', strict_slashes=False, methods=['PUT'])
def update_product_info():
    """ update the info of the product """
    jwt_token = request.cookies.get("seller_token")
    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    if 'type' not in data or data['type'] != 'seller':
        return jsonify({"state": "Not Authorized"}), 403

    seller_id = data['data_1']
    json_data = request.json

    if 'product_id' not in json_data:
        return jsonify({'state': 'bad_request'}), 400

    allowed_list = ['price', 'description', 'name', 'amount', 'photo']

    product = storage.get(Product, json_data['product_id'])

    if product is None:
        return jsonify({"state": "product is not found"}), 404

    if product.seller_id != seller_id:
        return jsonify({"state": "You are not the owner of the product"}), 403 


    name = product.name

    if 'name' in json_data:
        result = storage.get_with_one_attribute(Product, "name",json_data['name'])

        if result is not None:
            return jsonify({"state": "name already exists"}), 200

        name = json_data['name']

    for key, value in json_data.items():
        if key in allowed_list:
            if key == 'photo':
                photo_url = f"/static/{name}.jpg"
                if photo_url != product.photo_url:
                    if os.path.exists(f'.{product.photo_url}'):
                        os.remove(f'.{product.photo_url}')

                with open(f'.{photo_url}', 'wb') as file:
                    file.write(pybase64.b64decode(json_data['photo']))
                product.photo_url = photo_url
            else:
                setattr(product, key, value)

    product.save()

    return jsonify({"state": "the product is updated"}), 200


@app_views.route('/product_info', strict_slashes=False, methods=['GET'])
def get_product_info():
    """ get the info of the product """

    product_name = request.args.get('name')

    if product_name is None:
        return jsonify({'state': 'bad_request'}), 400

    product_name = product_name.strip()
    product = storage.get_with_one_attribute(Product, "name", product_name)

    if product is None:
        return jsonify({"state": "product is not found"}), 404

    product_data = product.to_dict()
    del product_data['_sa_instance_state']
    del product_data['seller_id']

    return jsonify(product_data), 200


@app_views.route('/product_not_exist', strict_slashes=False, methods=['DELETE'])
def delete_product_info():
    """ delete the info of the product """
    jwt_token = request.cookies.get("seller_token")
    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    if 'type' not in data or data['type'] != 'seller':
        return jsonify({"state": "Not Authorized"}), 403


    seller_id = data['data_1']
    json_data = request.json

    if 'product_id' not in json_data:
        return jsonify({'state': 'bad_request'}), 400

    product = storage.get(Product, json_data['product_id'])

    if product is None:
        return jsonify({"state": "product is not found"}), 404

    if product.seller_id != seller_id:
        return jsonify({"state": "You are not the owner of the product"}), 403

    if os.path.exists(f".{product.photo_url}"):
        os.remove(f".{product.photo_url}")

    products, orders = storage.get_all_item_id(User_Product, "product_id",json_data['product_id'])

    if len(orders) != 0:
        for order in orders:
            storage.delete(order)
        storage.save()


    storage.delete(product)
    storage.save()

    return jsonify({"state": "the product is deleted"}), 200


@app_views.route('/seller_products_info', strict_slashes=False, methods=['GET'])
def get_seller_products_info():
    """ get the info of the product """
    jwt_token = request.cookies.get("seller_token")
    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    if 'type' not in data or data['type'] != 'seller':
        return jsonify({"state": "Not Authorized"}), 403


    seller_id = data['data_1']


    products = storage.get_all_products(Product, 'seller_id', seller_id)

    if products == {}:
        return jsonify({"state": "there are not any products"}), 404

    return jsonify(products), 200
