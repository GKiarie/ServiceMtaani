#!/usr/bin/python3

from models.base_model import BaseModel
from models.client import Client
from models.mechanic import Mechanic
from models.vendor import Vendor
from models.bid import Bid
from models.job import Job
from models.order import Order
from models.image import Image
from models.part import Part
from models.review import Review
from models.vehicle import Vehicle
from models import storage

if __name__ == "__main__":
    client1 = Client(first_name="first", last_name="last", email="firstlast@email.com", password="pwd2023", phone_number=84823)
    client1.save()
