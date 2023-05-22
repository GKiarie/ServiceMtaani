#!/usr/bin/python3
"""Class for orders"""

from base_model import BaseModel, Base

class Order(BaseModel, Base):
    """Order attributes"""
    client_id = ""
    status = True

    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)