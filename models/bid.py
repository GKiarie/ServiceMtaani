#!/usr/bin/python3
"""
Class Bids
"""

from base_model import BaseModel, Base
from sqlalchemy import String, Integer, Column, ForeignKey

class Bid(BaseModel, Base):
    """Bid attributes"""

    __tablename__ = 'bids'
    mechanic_id = Column(String(50), ForeignKey('mechanic.id'), nullable=False)
    job_id  = Column(String(50), ForeignKey('jobs.id'), nullable=Flase)
    bid_amount = Column(Integer, nullable=False), default=0)

    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)