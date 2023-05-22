#!/usr/bin/python3
"""Clients class"""

from base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class Client(BaseModel, Base):
    """Define the variables that relate to the client"""
    __tablename__ = 'clients'
    id = Column(String(60), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    phone_number = Column(Integer, nullable=False, default=0)
    vehicles = relationship("Vehicle", backref="clients", cascade="all, delete, delete-orphan")
    orders = relationship("Order", backref="clients", cascade="all, delete, delete-orphan")
    jobs = relationship("Job", backref="clients", cascade="all, delete, delete-orphan")
    reviews = relationship("Review", backref="clients", cascade="all, delete, delete-orphan")


    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)