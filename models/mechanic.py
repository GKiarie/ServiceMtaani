#!/usr/bin/python3
"""
Class for mechanics
"""

from base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer

class Mechanic(BaseModel, Base):
    __tablename__ = "mechanic"
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    phone_number = Column(Integer, nullable=False)
    business_name = Column(String(60))
    jobs_compeleted = Column(Integer, nullable=False, default=0)
    rating = Column(Integer, nullable=False, default=0)
    specialization = Column(String(60))

    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)