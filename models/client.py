#!/usr/bin/python3
"""Clients class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class Client(BaseModel, Base):
    """Define the variables that relate to the client"""
    __tablename__ = 'clients'
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(50), nullable=False)
    phone_number = Column(Integer, nullable=False, default=0)
    vehicles = relationship("Vehicle", backref="client", cascade="all, delete, delete-orphan")
    orders = relationship("Order", backref="client", cascade="all, delete, delete-orphan")
    jobs = relationship("Job", backref="client", cascade="all, delete, delete-orphan")
    reviews = relationship("Review", backref="client", cascade="all, delete, delete-orphan")


    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)