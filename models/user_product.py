#!/usr/bin/python3
""" user module """
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Table, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base import Base, BaseModel


class User(BaseModel, Base):
    """ User class """

    __tablename__ = 'users'
    email = Column(String(128), nullable=False, unique=True)
    photo_url = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False)
    phone_number = Column(String(128), nullable=True)
    address = Column(String(128), nullable=True)
    relationship('User_Product', cascade='all, delete-orphan', backref='user')

    def __init__(self, *args, **kwargs):
        """ initializes user """
        super().__init__(*args, **kwargs)


class Product(BaseModel, Base):
    """ Product class """
    __tablename__ = 'products'
    description  = Column(String(128), nullable=False)
    photo_url = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False, unique=True, index=True)
    price = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    seller_id = Column(String(60), ForeignKey('sellers.id'))
    relationship('User_Product', backref='product')
    relationship('Cart_Product', backref='product')

    def __init__(self, *args, **kwargs):
        """initializes products"""
        super().__init__(*args, **kwargs)


class User_Product(BaseModel, Base):
    """ user_product """
    __tablename__ = 'user_product'

    user_id = Column(String(60), ForeignKey('users.id'))
    product_id = Column(String(60), ForeignKey('products.id'))
    amount = Column(Integer, nullable=False)
    payment_type = Column(String(60), nullable=False)
    states = Column(String(60), nullable=True)

    def __init__(self, *args, **kwargs):
        """initializes products"""
        super().__init__(*args, **kwargs)
