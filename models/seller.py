#!/usr/bin/python3
""" seller module """
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Table, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base import Base, BaseModel


class Seller(BaseModel, Base):
    """ seller class """
    __tablename__ = 'sellers'
    email = Column(String(128), nullable=False)
    photo_url = Column(String(128), nullable=False)
    name = Column(String(128), nullable=True)
    phone_number = Column(String(128), nullable=True)
    address = Column(String(128), nullable=True)


    def __init__(self, *args, **kwargs):
        """initializes products"""
        super().__init__(*args, **kwargs)

