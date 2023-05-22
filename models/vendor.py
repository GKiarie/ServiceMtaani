#!/usr/bin/python3
"""
Class for vendors
"""

from base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey

class Vendor(BaseModel, Base):
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    phone_number = Column(Integer, nullable=False)
    business_name = Column(String(100), nullable=False)
    orders_compeleted = Column(Integer, default=0, nullable=False)
    rating = Column(Integer, default=0, nullable=False)
    
    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)