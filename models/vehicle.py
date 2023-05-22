#!/usr/bin/python3
"""
Class for vehicles owned by client
"""

from base_model import BaseModel, Base

class Vehicle(BaseModel, Base):
    """Vehicle attributes"""
    client_id = ""
    make = ""
    model = ""
    body_type = ""
    year_of_manufacture = 0
    
    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)