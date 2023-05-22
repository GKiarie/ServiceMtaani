#!/usr/bin/python3

"""
Reviews Class
"""

from base_model import BaseModel, Base


class Review(BaseModel):
    """Review attributes"""
    client_id = ""
    vendor_id = ""
    mechanic_id = ""
    description = ""
    rating = 0

    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)