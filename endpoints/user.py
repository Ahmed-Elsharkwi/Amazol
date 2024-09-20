#!/usr/bin/python3
""" user api """
from endpoints import app_views
from models.user_product import User
from models.start import storage
from flask import jsonify, request
from utils.jwt_encoding_decoding_method import verify_jwt

@app_views.route('/new_user',  methods=['POST'], strict_slashes=False)
def add_user():
    """ add_new_user """
    user_data = request.json
    if "email" not in user_data or "name" not in user_data or "photo_url" not in user_data:
        return jsonify({"state": "bad request"}), 400

    result = storage.get_with_one_attribute(User, "email",user_data['email'])

    if result is not None:
        return jsonify({"state": "user already exists"}), 200

    new_user = User(**user_data)

    storage.new(new_user)
    storage.save()
    return jsonify({"state": new_user.id}), 200


@app_views.route('/user_info', methods=['GET'], strict_slashes=False)
def get_user():
    """ get the user info """
    jwt_token = request.cookies.get("token")
    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    user_id = data['data_1']
    user = storage.get(User, user_id)

    if user is None:
        return jsonify({"state": "user is not found"}), 404

    user_data = user.to_dict()
    del user_data['_sa_instance_state']

    if user_data["phone_number"] is None:
        user_data['phone_number'] = "no phone number was found"
    if user_data["address"] is None:
        user_data['address'] = "no address was found"

    return jsonify(user_data), 200


@app_views.route('/new_user_info' ,  methods=['PUT'], strict_slashes=False)
def update_user_info():
    """ update the info of the user """
    allowed_data = ['phone_number', 'address']
    jwt_token = request.cookies.get("user_token")
    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    user_id = data['data_1']
    user = storage.get(User, user_id)

    if user is None:
        return jsonify({"state": "user is not found"}), 404

    for data in request.json:
        if data in allowed_data:
            setattr(user, data, request.json[data])
    user.save()

    return jsonify("okay"), 200


@app_views.route('/user_not_exist' ,  methods=['DELETE'], strict_slashes=False)
def delete_user():
    """ delete the user """
    jwt_token = request.cookies.get("user_token")
    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    user_id = data['data_1']
    user = storage.get(User, user_id)

    if user is None:
        return jsonify({"state": "user is not found"}), 404

    storage.delete(user)
    storage.save()
    return jsonify("okay"), 200
