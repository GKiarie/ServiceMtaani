#!/usr/bin/python3
"""Module for the parts class"""

from base_model import BaseModel, Base

class Part(BaseModel, Base):
    """Part attributes"""
    vendor_id = ""
    part_name = ""
    part_description = ""
    part_price = 0
    
    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)
    