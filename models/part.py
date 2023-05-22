#!/usr/bin/python3
"""Module for the parts class"""

from base_model import BaseModel, Base
from sqlalchemy import String, Column, Integer, ForeignKey

class Part(BaseModel, Base):
    """Part attributes"""
    __tablename__ = "parts"
    vendor_id = Column(String(60), ForeignKey('vendors.id'), nullable=False)
    part_name = Column(String(60), nullable=False)
    part_description = Column(String(120))
    part_price = Column(Integer, nullable=False, default=0)
    part_images=Column(String(200))
    # /root/images/part345
    
    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)
    