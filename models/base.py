#!/usr/bin/env python3
""" base model """
import uuid
from datetime import datetime
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
import models

Base = declarative_base()

class BaseModel():
    """ Base Model """
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


    def __init__(self, *args, **kwargs):
        """ create instance attributes """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    self.__dict__[key] = value

            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """ return the string represantation of an object """
        return "[{}] ({}) {}".format(str(self.__class__.__name__), str(
            self.id), self.__dict__)

    def save(self):
        """ update the public instance attribute updated_at 
        with the current date
        """
        self.updated_at = datetime.utcnow()
        models.start.storage.save()

    def to_dict(self):
        """ returns a dictionary containing all keys/values 
        of __dict__ of the instance"""
        new_dict = self.__dict__.copy()
        #new_dict["__class__"] = self.__class__.__name__
        new_dict["updated_at"] = new_dict["updated_at"].strftime(
                "%Y-%m-%dT%H:%M:%S.%f")
        new_dict["created_at"] = new_dict["created_at"].strftime(
                "%Y-%m-%dT%H:%M:%S.%f")
        return new_dict
