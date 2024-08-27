#!/usr/bin/python3
""" cart module """
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Table, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base import Base, BaseModel


class Cart(BaseModel, Base):
    """ Cart class """
    __tablename__ = 'carts'
    user_id = Column(String(60), ForeignKey('users.id'), unique=True)
    relationship('Cart_Product', backref='cart')

    def __init__(self, *args, **kwargs):
        """initializes products"""
        super().__init__(*args, **kwargs)


class Cart_Product(Base, BaseModel):
    """ product_cart """
    __tablename__ = 'product_cart'

    cart_id = Column(String(60), ForeignKey('carts.id'))
    product_id = Column(String(60), ForeignKey('products.id'))

    def __init__(self, *args, **kwargs):
        """initializes products"""
        super().__init__(*args, **kwargs)
