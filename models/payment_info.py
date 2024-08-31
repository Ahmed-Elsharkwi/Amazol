#!/usr/bin/python3
""" payment info module """
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Table, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from models.base import Base, BaseModel


class Payment(BaseModel, Base):
    """ payment module """
    __tablename__ = 'payment_info'
    number = Column(String(60), nullable=False)
    cvv = Column(Integer, nullable=False)
    expiry_date = Column(String(60), nullable=False)
    holder_name = Column(String(60), nullable=False)
    payment_type = Column(String(60), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'))

    def __init__(self, *args, **kwargs):
        """ initializes user """
        super().__init__(*args, **kwargs)
