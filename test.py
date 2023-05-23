#!/usr/bin/python3

from models.base_model import BaseModel
from models.client import Client

if __name__ == "__main__":
    client1 = Client(first_name="first", last_name="last", email="firstlast@email.com", password="pwd2023", phone_number=84823)
    client1.save()
