#!/usr/bin/python3
"""handles api actns for bids"""
from api.v1.views import app_views
from models import storage
from models.job import Job
from models.bid import Bid
from flask import abort, request, jsonify

@app_views.route('/jobs/<job_id>/bids', strict_slashes=False,
                 methods=["GET", "POST"])
def get_bids_job_id(job_id):
    job_objs = storage.all(Job).values()
    job_exists = False
    for job_obj in job_objs:
        if job_obj.id == job_id:
            job_exists = True
            break
    if not job_exists:
        abort(404)
    if request.method == "GET":
        bid_objs = storage.all(Bid).values()
        list_dict = [obj.to_dict() for obj in bid_objs if obj.job_id == job_id]
        return jsonify(list_dict), 200
    elif request.method == "POST":
        my_dict = request.get_json()
        if not my_dict:
            abort(400, "Not a JSON")
        if not my_dict.get('mechanic_id'):
            abort(400, "Missing mechanic id")
        else:
            my_dict["job_id"] = job_id
            obj = Bid(**my_dict)
            obj.save()
            return jsonify(obj.to_dict()), 201

@app_views.route('/jobs/<job_id>/bids/<bid_id>', strict_slashes=False,
                 methods=["GET", "PUT", "DELETE"])
def get_bids_job_id(job_id, bid_id):
    job_objs = storage.get(Job, job_id)
    bid_objs = storage.get(Bid, bid_id)    
    if job_objs is None or bid_objs is None:
        abort(404, "Invalid job or bid id")

    if request.method == "GET":
        bid_objs = storage.all(Bid).values()
        list_dict = [obj.to_dict() for obj in bid_objs if obj.job_id == job_id]
        return jsonify(list_dict), 200
    
    elif request.method == "POST":
        my_dict = request.get_json()
        if not my_dict:
            abort(400, "Not a JSON")
        if not my_dict.get('mechanic_id'):
            abort(400, "Missing mechanic id")
        else:
            my_dict["job_id"] = job_id
            obj = Bid(**my_dict)
            obj.save()
            return jsonify(obj.to_dict()), 201