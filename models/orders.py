#!/usr/bin/python3
"""Class for orders"""

from base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

class Order(BaseModel, Base):
    """Order attributes"""
    client_id = Column(String(60), ForeignKey('client.id'), nullable=False)
    status = True

    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)