#!/usr/bin/python3
"""
Class for vendors
"""

from base_model import BaseModel, Base

class Vendor(BaseModel, Base):
    first_name = ""
    last_name = ""
    email = ""
    phone_number = 0
    business_name = ""
    orders_compeleted = 0
    rating = 0
    
    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)