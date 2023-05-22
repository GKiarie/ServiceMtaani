#!/usr/bin/python3
"""This module contains the Base Class for Clients, Mechanics
and Vendors Classses
"""
from models.engine import storage
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel():
    """Class to base all other classes on"""
    def __init__(self, **kwargs):
        if kwargs:
            if id not in kwargs.keys():
                self.id = str(uuid4())
                self.created_at = datetime.now()
                self.updated_at = self.created_at
                for key, value in kwargs.items():
                    setattr(self, key, value)
                # storage.new(self)
    
    def __str__(self):
        """Return a string representation of the object"""
        attributes_dict = self.__dict__.copy()
        attributes_dict['created_at'] = attributes_dict['created_at'].strftime("%m/%d/%Y, %H:%M:%S")
        attributes_dict['updated_at'] = attributes_dict['updated_at'].strftime("%m/%d/%Y, %H:%M:%S")
        return f"Class: {self.__class__.__name__}, ID: {self.id}, DETAILS: {attributes_dict}"
    
    def to_str(self):
        attributes_dict = self.__dict__.copy()
        attributes_dict['created_at'] = attributes_dict['created_at'].strftime("%m/%d/%Y, %H:%M:%S")
        attributes_dict['updated_at'] = attributes_dict['updated_at'].strftime("%m/%d/%Y, %H:%M:%S")
        return f"Class: {self.__class__.__name__}, ID: {self.id}, DETAILS: {attributes_dict}"
    
    def save(self):
        """Save the object to the database"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()
    
    def delete(self):
        """Delete the object from the database"""
        storage.delete(self)
    