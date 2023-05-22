#!/usr/bin/python3
"""
Jobs class
"""

from base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

class Job(BaseModel, Base):
    """Job attributes"""
    client_id = Column(String(60), ForeignKey('client.id'), nullable=False)
    job_title = Column(String(60), nullable=False)
    job_description = Column(String(120))
    status = False

    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)