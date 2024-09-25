#!/usr/bin/python3
""" main end point """

from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from authlib.integrations.flask_client import OAuth
from flask import Flask, make_response, jsonify, request, render_template, make_response
from flask_cors import CORS
from endpoints import app_views
from models.start import storage
from utils.jwt_encoding_decoding_method import create_jwt, verify_jwt
import re
from models.user_product import User
from models.seller import Seller
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.secret_key = 'i am good'
google_client_id = '420372669639-dqsfi064hhcne9rsp8c7sns70kg54j72.apps.googleusercontent.com'
google_client_secret = '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'
google_redirect_uri = 'http://localhost:3000/authorize'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=google_client_id,
    client_secret=google_client_secret,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=google_redirect_uri,
    client_kwargs={'scope': 'email profile'},
)


@app.route('/login')
def login():
    """
    check if there is token in request's cookies or not and also check if the token is valid or not.
    if there is any token the user will be redirected to the main page.
    if there is a token but it is valid the user
    or there no token the user will redirected to authorize end point
    """

    session['type'] = request.args.get('type')

    if session['type'] == 'user' or session['type'] is None:
        token_type = 'user_token'
    elif session['type'] == 'seller':
        token_type = 'seller_token'
    else:
        return jsonify({"state": "Don't change the type of the user"}), 200

    token = request.cookies.get(token_type)

    if (token is None) or (verify_jwt(token) is None):
        if request.args.get('next_page') is not None:
            session['next_page'] = request.args.get('next_page')

        redirect_uri = url_for('authorize', _external=True)
        return google.authorize_redirect(redirect_uri, prompt='consent')

    else:
        return redirect(url_for('get_main_page'))


@app.route('/authorize')
def authorize():
    """ 
    Get the google token and after that get the info of the google user.
    Check if the person is trying to log in as user or as seller and after
    that create a token for him.
    Check if there is page which need to be redirected to after finishing the sign in process.
    """

    try:
        token = google.authorize_access_token()
        session['google_token'] = token
        google_token = session['google_token']

        resp = (google.get('https://www.googleapis.com/oauth2/v1/userinfo', token=google_token)).json()
        type_object = session['type']
        print(type_object)
        if type_object is None:
                type_object = 'user'

        if type_object == 'user' or type_object is None:
            Class_name = User
            url = 'http://localhost:5000/Amazol/new_user'
            token_type = 'user_token'
        else:
            Class_name = Seller
            url = 'http://localhost:5000/Amazol/new_seller'
            token_type = 'seller_token'

        Object = storage.get_with_one_attribute(Class_name,'email', resp['email']) 

        if Object is None:
            google_data = {
                    "email": resp["email"], 
                    "name": resp["name"], 
                    "photo_url": resp["picture"]
                    }

            data = requests.post(url, json = google_data)
            Object_id = data.json()['state']
        else:
            allowed_data = ['phone_number', 'address']
            for data in resp:
                if data in allowed_data:
                    setattr(Object, data, request.json[data])
            Object.save()
            Object_id = Object.id


        token = create_jwt({"data_1": Object_id, 'exp': datetime.utcnow() + timedelta(seconds=1200), 'type': type_object})

        if 'next_page' in session:
            next_page = session['next_page']
            del session['next_page']
            response = make_response(redirect(next_page))
        
        elif 'next' in session:
            next_url = session['next']
            del session['next']
            response = make_response(redirect(next_url))
        else:
            response = make_response(jsonify({"status": "okay"}), 200)

        del session['type']
        response.set_cookie(token_type, token, samesite='None', secure=True)
        return response

    except KeyError as e:
        print(e)


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return jsonify({"status": "okay"}), 200

@app.route('/', methods=['GET'], strict_slashes=False)
def get_main_page():
    """ get home page """
    search_query = request.args.get('search_query')
    token = request.cookies.get('user_token')
    token_1 = request.cookies.get('seller_token')

    user_name = None
    seller_name = None

    if token is not None:
        if verify_jwt(token) is not None:
            data = requests.get('http://localhost:5000/Amazol/user_info', cookies={'token': token})
            user_name = data.json()['name']

    if token_1 is not None:
        if verify_jwt(token_1) is not None:
            data = requests.get('http://localhost:5000/Amazol/seller_info', cookies={'token': token_1})
            seller_name = data.json()['name']
     
    return render_template('home.html', user=user_name, seller=seller_name, search_query=search_query)

@app.route('/product_info', methods=['GET'], strict_slashes=False)
def print_message():
    """ get home page """
    product_name = request.args.get('product_name')
    token = request.cookies.get('user_token')
    token_1 = request.cookies.get('seller_token')

    user_name = None
    seller_name = None

    if token is not None:
        if verify_jwt(token) is not None:
            data = requests.get('http://localhost:5000/Amazol/user_info', cookies={'token': token})
            user_name = data.json()['name']

    if token_1 is not None:
        if verify_jwt(token_1) is not None:
            data = requests.get('http://localhost:5000/Amazol/seller_info', cookies={'token': token_1})
            seller_name = data.json()['name']

    if product_name is None:
        return jsonify("Product is not found"), 404

    return render_template('product.html', product_name=product_name, user=user_name, seller=seller_name)



@app.teardown_appcontext
def teardown(exc):
    """ hanle teardown_qppcontext """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ handler for 404 errors """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, threaded=True, debug=True)
