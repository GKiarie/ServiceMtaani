#!/usr/bin/python3
"""
Jobs class
"""

from base_model import BaseModel, Base

class Job(BaseModel, Base):
    """Job attributes"""
    client_id = ""
    job_title = ""
    job_description = ""
    status = False

    def __init__(self, **kwargs):
        """initialize the subclass using the superclass"""
        super().__init__(**kwargs)