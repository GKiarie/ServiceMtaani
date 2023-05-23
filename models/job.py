#!/usr/bin/python3
"""
Jobs class
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Boolean

class Job(BaseModel, Base):
    """Job attributes"""
    __tablename__ = "jobs"
    client_id = Column(String(60), ForeignKey('clients.id'), nullable=False)
    job_title = Column(String(200), nullable=False)
    job_description = Column(String(500))
    status = Column(Boolean, default=True)

    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)
