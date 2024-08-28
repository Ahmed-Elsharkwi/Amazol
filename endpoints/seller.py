#!/usr/bin/python3
""" user api """
from endpoints import app_views
from models.seller import Seller
from models.start import storage
from flask import jsonify, request
from utils.jwt_encoding_decoding_method import verify_jwt

@app_views.route('/new_seller',  methods=['POST'], strict_slashes=False)
def add_seller():
    """ add_new_seller """
    seller_data = request.json
    if "email" not in seller_data or "name" not in seller_data or "photo_url" not in seller_data:
        return jsonify({"state": "bad request"}), 403

    result = storage.get_with_one_attribute(Seller, "email",seller_data['email'])

    if result is not None:
        return jsonify({"state": "user already exists"}), 302

    new_seller = Seller(**seller_data)

    storage.new(new_seller)
    storage.save()
    return jsonify({"state": new_seller.id}), 200


@app_views.route('/seller_info', methods=['GET'], strict_slashes=False)
def get_seller():
    """ get the seller info """
    jwt_token = request.cookies.get("token")
    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    seller_id = data['data_1']

    if 'type' not in data or data['type'] != 'seller':
        return jsonify({'state': 'Not Authorized'}), 401

    seller = storage.get(Seller, seller_id)

    if seller is None:
        return jsonify({"state": "seller is not found"}), 403

    seller_data = seller.to_dict()
    del seller_data['_sa_instance_state']

    if seller_data["phone_number"] is None:
        seller_data['phone_number'] = "no phone number found"
    if seller_data["address"] is None:
        seller_data['address'] = "no address found"

    return jsonify(seller_data), 200


@app_views.route('/new_seller_info' ,  methods=['PUT'], strict_slashes=False)
def update_seller_info():
    """ update the info of the seller """
    allowed_data = ['phone_number', 'address']
    jwt_token = request.cookies.get("token")
    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    seller_id = data['data_1']

    if 'type' not in data or data['type'] != 'seller':
        return jsonify({'state': 'Not Authorized'}), 401

    seller = storage.get(Seller, seller_id)

    if seller is None:
        return jsonify({"state": "seller is not found"}), 403

    for data in request.json:
        if data in allowed_data:
            setattr(user, data, request.json[data])
    user.save()

    return jsonify("okay"), 200


@app_views.route('/seller_not_exist' ,  methods=['DELETE'], strict_slashes=False)
def delete_seller():
    """ delete the seller """
    jwt_token = request.cookies.get("token")
    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    seller_id = data['data_1']

    if 'type' not in data or data['type'] != 'seller':
        return jsonify({'state': 'Not Authorized'}), 401

    seller = storage.get(Seller, seller_id)

    if seller is None:
        return jsonify({"state": "seller is not found"}), 403

    storage.delete(seller)
    storage.save()
    return jsonify("okay"), 200
