#!/usr/bin/python3
"""Implement database storage"""
import models
from models.base_model import Base
from models.job import Job
from models.client import Client
from models.bid import Bid
from models.mechanic import Mechanic
from models.order import Order
from models.part import Part
from models.review import Review
from models.vehicle import Vehicle
from models.vendor import Vendor
from models.image import Image
from sqlalchemy import create_engine as ce
from sqlalchemy.exc import IntegrityError
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
        self.__engine = ce('mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, dtbs), pool_pre_ping=True)
        # self.__engine = ce('mysql+mysqldb://admin:admin2023@localhost/service_mtaani', pool_pre_ping=True)

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
        try:
            self.__session.commit()
        except Exception as e:
            print("Error creating DB Entry")
            print()
            print(e)
            print()
            self.__session.rollback()

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
        if not cls:
            for item in classes:
                objs = self.__session.query(item).all()
                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj
        if cls in classes:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + "." + obj.id
                new_dict[key] = obj
        return new_dict

    def get(self, cls, id):
        """method to retrieve one object"""
        objs = self.all(cls).values()
        for obj in objs:
            if obj.id == id:
                return obj
        return None

    def find(self, cls=None, attr=None, val=None):
        """Return an instance for a db entry"""
        if cls in classes:
            obj = self.__session.query(cls).filter(getattr(cls, attr) == val).first()
        return obj

    def count(self, cls=None):
        """return count of the class passed
        total items in db if no class is passed"""
        obj_dict = self.all(cls)
        return len(obj_dict)

    def openjobs(self):
        """Return a list of open jobs"""
        jobs = self.__session.query(Job).filter(Job.status == True).all()
        return jobs
