#!/usr/bin/python3
"""
Class for mechanics
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class Mechanic(BaseModel, Base):
    __tablename__ = "mechanics"
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    phone_number = Column(Integer, nullable=False)
    business_name = Column(String(60))
    jobs_compeleted = Column(Integer, nullable=False, default=0)
    rating = Column(Integer, nullable=False, default=0)
    specialization = Column(String(60))
    bids = relationship("Bid", backref="mechanic", cascade="all, delete, delete-orphan")
    reviews = relationship("Review", backref="mechanic", cascade="all, delete, delete-orphan")

    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)
