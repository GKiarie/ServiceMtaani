#!/usr/bin/python3
"""Implement database storage"""
from models.base_model import Base
from models.job import Job
from models.client import Client
from models.bid import Bid
from models.mechanic import Mechanic
from models.orders import   Order
from models.part import Part
from models.review import Review
from models.vehicle import Vehicle
from models.vendor import Vendor
from models.image import Image
from sqlalchemy import create_engine as ce
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv

classes=[Job, Client, Bid, Mechanic, Order, Part, Review, Vehicle, Vendor, Image]

class DBStorage:
    """Database Storage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize db"""
        user = getenv("MYSQL_USER")
        pwd = getenv("MYSQL_PWD")
        host = getenv("MYSQL_HOST")
        dtbs = getenv("MYSQL_DTBS")
        #self.__engine = ce(f'mysql+mysqldb://{user}:{pwd}@{host}/{dtbs}', pool_pre_ping=True)
        self.__engine = ce('mysql+mysqldb://admin:admin2023@localhost/service_mtaani', pool_pre_ping=True)

    def reload(self):
        """Reload data in the db"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session

    
    def new(self, obj):
        """Create a new object"""
        self.__session.add(obj)

    def save(self):
        """Commit the session to the db"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object"""
        if obj:
            self.__session.delete(obj)

    def close(self):
        """Close the session"""
        self.__session.remove()

    def all(self, cls=None):
        """Retrieve all objects of a class"""
        new_dict = {}
        if cls in classes:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + "." + obj.id
                new_dict[key] = obj.to_str()
        return new_dict
