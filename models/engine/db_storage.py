#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import pymysql
pymysql.install_as_MySQLdb()
from models.base import BaseModel, Base
from models.user_product import User, Product, User_Product
from models.Cart import Cart, Cart_Product
from models.seller import Seller
from models.payment_info import Payment
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {
        "User": User, 
        "Product": Product, 
        "Cart": Cart, 
        'Cart_Product': Cart_Product, 
        'User_Product': User_Product,
        'Seller': Seller,
        'Payment': Payment
        }


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        self.__engine = create_engine('mysql+mysqldb://zol:Amozol@localhost/Amozol',  pool_pre_ping=True)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

    def get_with_one_attribute(self, cls, attribute, att_val):
        """
        Returns the object based on the class name and its attribute, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if (value.__dict__[attribute] == att_val):
                return value

        return None

    def get_with_two_attribute(self, cls, attribute_1, att_1_val, attribute_2, att_2_val):
        """
        Returns the object based on the class name and its two attributes, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if (value.__dict__[attribute_1] == att_1_val) and (value.__dict__[attribute_2] == att_2_val):
                return value

        return None

    def get_all_item_id(self, cls, attribute, att_id):
        """ get all items with a specific id """
        if cls not in classes.values():
            return None

        data = []
        objects = []
        all_cls = self.all(cls)
        for value in all_cls.values():
            if value.__dict__[attribute] == att_id:
                data.append(value.product_id)
                objects.append(value)

        products = self.__session.query(Product).filter(Product.id.in_(data)).all()
        return products, objects

    def get_all_products(self, cls, attribute, att_id):
        """ get all items with a specific id """
        if cls not in classes.values():
            return None

        data = {}
        all_cls = self.all(cls)
        for value in all_cls.values():
            if value.__dict__[attribute] == att_id:
                data_value = value.to_dict()
                del data_value['_sa_instance_state']
                if cls == Product:
                    del data_value['seller_id']
                else:
                    del data_value['user_id']

                data[value.id] = data_value

        return data
