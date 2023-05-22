#!/usr/bin/python3

"""
Reviews Class
"""

from base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer


class Review(BaseModel):
    """Review attributes"""
    __tablename__ = "reviews"
    client_id = Column(String(60), ForeignKey('clients.id'), nullable=False)
    vendor_id = Column(String(60), ForeignKey('vendor.id'))
    mechanic_id = Column(String(60), ForeignKey('mechanic.id'))
    description = Column(String(120))
    rating = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)