#!/usr/bin/python3
""" payment api """
from utils.credit_card_validation import validate_credit_card_num, get_card_type, verify_date 
from endpoints import app_views
from models.payment_info import Payment
from models.user_product import User
from models.start import storage
from flask import jsonify, request
from utils.jwt_encoding_decoding_method import verify_jwt

@app_views.route('/new_payment_method',  methods=['POST'], strict_slashes=False)
def add_payment_method():
    """ add_new_payment_method """
    jwt_token = request.cookies.get("user_token")

    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    user_id = data['data_1']
    if 'type' not in data or data['type'] != 'user':
        return jsonify({"state": "Not Authorized"}), 403


    payment_method_data = request.json
    if ("number" not in payment_method_data) or (
            "holder_name" not in payment_method_data) or (
                    "cvv" not in payment_method_data) or (
                            "month" not in payment_method_data) or (
                                    "year" not in payment_method_data):
        return jsonify({"state": "bad request"}), 400

    result = storage.get_all_products(Payment, "user_id", user_id)

    if len(result) == 3:
        return jsonify({"state": "The maximum number of payment methods is 3"}), 400

    for payment_way in result.values():
        print(payment_way)
        if payment_way['number'] == payment_method_data['number']:
            return jsonify({"state": "payment method already exists"}), 400

    respond = validate_credit_card_num(payment_method_data['number'])

    if respond == "Vaild number":
        respond = get_card_type(payment_method_data['number'], 
                payment_method_data['cvv'])
        payment_method_data['payment_type'] = respond


        if respond != "Invalid cvv":
            respond = verify_date(payment_method_data['month'], payment_method_data['year'])

            if respond == "Valid card":
                payment_method_data['user_id'] = user_id
                payment_method_data['expiry_date'] = f'{payment_method_data["month"]}/{payment_method_data["year"]}'
                del payment_method_data['month']
                del payment_method_data['year']
                new_payment_method = Payment(**payment_method_data)

                storage.new(new_payment_method)
                storage.save()
                return jsonify({"state": "payment method is added", "id": new_payment_method.id}), 200

    return jsonify({"state": respond}), 400


@app_views.route('/payment_info', methods=['GET'], strict_slashes=False)
def get_payment():
    """ get the payment info """
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

    payments = storage.get_all_products(Payment, 'user_id', user_id)

    if len(payments) == 0:
        return jsonify({"state": "There are not any payment methods"}), 404

    data = {}
    for key, value in payments.items():
        date = value['expiry_date'].split('/')
        if verify_date(date[0], date[1]) == "Valid card":
            number = value["number"]
            number = number[len(number) - 5 : len(number) - 1]
            data[key] = {
                    "number": f'{value["payment_type"]} *{number}',
                    "holder_name": value["holder_name"],
                    "expiry_date": value["expiry_date"],
                    "payment_type": value["payment_type"],
                    "billing_address": user.address,
                    "id": value['id']
                    }

    return jsonify(data), 200


@app_views.route('/new_payment_info' ,  methods=['PUT'], strict_slashes=False)
def update_payment_info():
    """ update the info of the payment """
    allowed_data = ['holder_name', 'expiry_date']
    jwt_token = request.cookies.get("user_token")

    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    user_id = data['data_1']

    if 'type' not in data or data['type'] != 'user':
        return jsonify({"state": "Not Authorized"}), 403


    payment_method = storage.get_with_two_attribute(Payment, 'user_id', user_id, 'id', request.json['id'])

    if payment_method is None:
        return jsonify({"state": "payment_method is not found"}), 404

    if verify_date(request.json['month'], request.json['year']) == "Valid card":
        request.json['expiry_date'] = f'{request.json["month"]}/{request.json["year"]}'
        for data in request.json:
            if data in allowed_data:
                setattr(payment_method, data, request.json[data])
        payment_method.save()
    
        return jsonify({"state": "the payment method in updated"}), 200

    return jsonify("Invalid date"), 200

@app_views.route('/payment_not_exist' ,  methods=['DELETE'], strict_slashes=False)
def delete_payment():
    """ delete the payment method """
    jwt_token = request.cookies.get("user_token")

    data = None
    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    user_id = data['data_1']
    if 'type' not in data or data['type'] != 'user':
        return jsonify({"state": "Not Authorized"}), 403

    payment_method = storage.get_with_two_attribute(Payment, 'user_id', user_id, 'id', request.json['id'])

    if payment_method is None:
        return jsonify({"state": "payment_method is not found"}), 404

    storage.delete(payment_method)
    storage.save()
    return jsonify({"state": "the payment method is deleted"}), 200
