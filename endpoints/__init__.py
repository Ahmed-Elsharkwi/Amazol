#!/usr/bin/python3
""" blue print api """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/Amazol')

from endpoints.user import *
from endpoints.seller import *
from endpoints.product import *
from endpoints.user_product import *
