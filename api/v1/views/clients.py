#!/usr/bin/python3
"""Handles client api"""


from api.v1.views import app_views
from models import storage
from models.client import Client
from flask import request, jsonify, abort

@app_views.route("/clients", methods=["GET", "POST"],strict_slashes=False)
@app_views.route("/clients/<client_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_all_clients(client_id=None):
    all_clients = storage.all(Client).values()

    clients_list = [client.to_dict() for client in all_clients]

    if not client_id:
        if request.method == "GET":
            return jsonify(clients_list), 200

        elif request.method == "POST":
            my_dict = request.get_json()
            if not my_dict:
                abort(400, "JSON missing")
            if my_dict.get("first_name") is None or \
                my_dict.get("last_name") is None or \
                my_dict.get("phone_number") is None or \
                my_dict.get("password") is None or \
                my_dict.get("email") is None:
                abort(400, "Incomplete Information")

            else:
                client_obj = Client(**my_dict)
                client_obj.save()
                return jsonify(client_obj.to_dict()), 201
    else:
        client_obj = storage.get(Client, client_id)

        if not client_obj:
            abort(404, "Client not Found")

        if request.method == "GET":
            return jsonify(client_obj.to_dict()), 200

        elif request.method == "PUT":
            my_dict = request.get_json()

            if not my_dict:
                abort(400, "Invalid input")

            else:
                for key, val in my_dict.items():
                    setattr(client_obj, key, val)
                client_obj.save()
                return jsonify(client_obj.to_dict()), 201
        else:
            storage.delete(client_obj)
            storage.save()
            return jsonify({}), 200
