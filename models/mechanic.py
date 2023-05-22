#!/usr/bin/python3
"""
Class for mechanics
"""

from base_model import BaseModel, Base

class Mechanic(BaseModel, Base):
    first_name = ""
    last_name = ""
    email = ""
    phone_number = 0
    business_name = ""
    jobs_compeleted = 0
    rating = 0
    specialization = ""

    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)