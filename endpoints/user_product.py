#!/usr/bin/python3
""" product api """
from endpoints import app_views
from models.user_product import User_Product, User, Product
from models.start import storage
from flask import jsonify, request
from utils.jwt_encoding_decoding_method import verify_jwt
from datetime import datetime

@app_views.route('/new_order', strict_slashes=False, methods=['POST'])
def add_new_order():
    """ add new order to the user_product table """
    jwt_token = request.cookies.get("user_token")
    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401


    user_id = data['data_1']

    if 'type' not in data or data['type'] != 'user':
        return jsonify({"state": "Not Authorized"}), 403
    
    user = storage.get_with_one_attribute(User, "id",user_id)

    if user.address is None or user.phone_number is None:
        return jsonify({"state": "please add your address and your phone number in your profile page"}), 400

    json_data = request.json

    if ("amount" not in json_data) or ('product_id' not in json_data) or (
            'payment_type' not in json_data):

            return jsonify({"state": "bad request"}), 400

    product = storage.get_with_one_attribute(Product, "id",json_data['product_id'])

    if product is None:
        return jsonify({"state": "product is not found"}), 404

    order = storage.get_with_two_attribute(
            User_Product, 'product_id', json_data['product_id'], 'user_id', user_id)

    if (order is not None) and (order.created_at.hour == datetime.utcnow().hour):

        return jsonify({'state': 'order already exists'}), 200

    message = f'The required amount is not avalible, the available amount is {product.amount}'

    if int(json_data['amount']) > product.amount:
        return jsonify({'state': message}) , 404

    json_data['user_id'] = user_id
    new_order = User_Product(**json_data)
    product.amount = product.amount - int(json_data['amount'])

    product.save()
    storage.new(new_order)
    storage.save()

    return jsonify({"state": "order is placed"}), 200


@app_views.route('/orders_info', strict_slashes=False, methods=['GET'])
def get_orders_info():
    """ get the info of the orders """
    jwt_token = request.cookies.get("user_token")
    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401


    user_id = data['data_1']

    if 'type' not in data or data['type'] != 'user':
        return jsonify({"state": "Not Authorized"}), 403


    user = storage.get_with_one_attribute(User, "id",user_id)

    products, orders = storage.get_all_item_id(User_Product, 'user_id', user_id)

    if len(products) == 0 or len(orders) == 0:
        return jsonify({'state': 'There are not any orders'}), 404

    data = {}
    for order in orders:
        for product in products:
            if order.product_id == product.id:
                Total_price = order.amount * product.price
                data[order.id] = {
                        'Total_price': Total_price,
                        'product_name': product.name,
                        'product_id': product.id,
                        'product_photo_url': product.photo_url,
                        'order_date': order.created_at,
                        'payment_method': order.payment_type,
                        'order_amount': order.amount,
                        'billing_address': user.address
                        }

    return jsonify(data), 200


@app_views.route('/order_not_exist', strict_slashes=False, methods=['DELETE'])
def delete_order_info():
    """ delete the info of the order """
    jwt_token = request.cookies.get("user_token")
    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    user_id = data['data_1']

    if 'type' not in data or data['type'] != 'user':
        return jsonify({"state": "Not Authorized"}), 403

    json_data = request.json


    if 'product_id' not in json_data:
        return jsonify({'state': 'product_id is missing'}), 400

    product = storage.get_with_one_attribute(Product, "id",json_data['product_id'])

    if product is None:
        return jsonify({"state": "product is not found"}), 404

    order = storage.get_with_two_attribute(
            User_Product, 'product_id', json_data['product_id'], 'user_id', user_id)

    if order is  None:
        return jsonify({'state': 'order does not exist'}), 404

    product.amount += order.amount
    storage.delete(order)
    product.save()
    storage.save()

    return jsonify({"state": "the product is deleted"}), 200
