#!/usr/bin/python3
"""
Class for vendors
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class Vendor(BaseModel, Base):
    __tablename__ = "vendors"
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False, unique=True)
    phone_number = Column(Integer, nullable=False)
    business_name = Column(String(100), nullable=False)
    orders_completed = Column(Integer, default=0, nullable=False)
    rating = Column(Integer, default=0, nullable=False)
    parts = relationship("Part", backref="vendor", cascade="all, delete, delete-orphan")
    reviews  = relationship("Review", backref="vendor", cascade="all, delete, delete-orphan")

    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)
