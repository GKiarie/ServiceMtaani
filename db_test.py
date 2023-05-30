#!/usr/bin/python3

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
    client1 = Client(first_name="Monty", last_name="Python", \
                     email="montypython@gmail.com", password="pwd2023", \
                        phone_number="0743284823")
    client1.save()
    mech1 = Mechanic(first_name="Jake", last_name="Kim", \
                     email="jakekim@email.com", password="fakepassword", phone_number="0789097789", \
                        business_name="Jake Garage",  jobs_completed=0, \
                            rating=0)
    mech1.save()
    vendor1 = Vendor(first_name="Jon", last_name="Snow", email="jonsnow@gmail.com", \
                     phone_number="0722663664", business_name="Jon Recovery", password="fakepassword")
    vendor1.save()
    vehicle1 = Vehicle(client_id=client1.id, make="Toyota", model="Camry", \
                       body_type="Sedan", year_of_manufacture="2012")
    vehicle1.save()
    job1 = Job(client_id=client1.id, job_title="Carwash", job_description="Major carwash. Car very dirty")
    job1.save()
    bid1 = Bid(mechanic_id=mech1.id, job_id=job1.id, bid_amount=200)
    bid1.save()
    part1 = Part(vendor_id=vendor1.id, part_name="Headlights", part_price=20000)
    part1.save()
    image1 = Image(part_id=part1.id, image_path="/Downloads/headlights.png")
    image1.save()
    rev1 = Review(client_id=client1.id, mechanic_id=mech1.id, description="Good guy", rating=5)
    rev1.save()
    order1 = Order(client_id=client1.id)
    order1.save()
    order1.parts.append(part1)
    order1.save()