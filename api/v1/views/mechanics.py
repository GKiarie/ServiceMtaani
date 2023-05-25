#!/usr/bin/python3
"""Create API routes for the mechanics
Routes: /mechanics/<mechanic_id>
      : /mechanics/<mechanic_id>/reviews/<review_id>
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models.mechanic import Mechanic
from models.review import Review
from models import storage


@app_views.route('/mechanics', \
                 methods=["GET", "POST"], strict_slashes=False)
@app_views.route('/mechanics/<mechanic_id>', \
                 methods=["GET", "PUT", "DELETE"])
def get_mechanics(mechanic_id=None):
    all_mechs = storage.all(Mechanic)
    if not mechanic_id:
        if request.method == "GET":
            mechs_list = [mech.to_dict() for mech in all_mechs.values()]
            return jsonify(mechs_list), 200
        if request.method == "POST":
            mech_attrs = request.get_json()
            if not mech_attrs or type(mech_attrs) is not dict:
                abort(400, "Invalid input")
            if mech_attrs.get("first_name") is None or \
                mech_attrs.get("last_name") is None or \
                    mech_attrs.get("email") is None or \
                        mech_attrs.get("password") is None:
                abort(400, "Incomplete information")
            mech_obj = Mechanic(**mech_attrs)
            mech_obj.save()
            return jsonify(mech_obj.to_dict()), 201
    
    if mechanic_id:
        mech_obj = storage.get(Mechanic, mechanic_id)
        if not mech_obj:
            abort(404, "Mechanic not found")
        if request.method == "GET":
            return jsonify(mech_obj.to_dict()), 200
        if request.method == "PUT":
            mech_attributes = request.get_json()
            if not mech_attributes or type(mech_attributes) is not dict:
                abort(400, "Invalid input")
            for k, v in mech_attributes.items():
                setattr(mech_obj, k, v)
            mech_obj.save()
            return jsonify(mech_obj.to_dict()), 201
        if request.method == "DELETE":
            mech_obj.delete()
            storage.save()
            return jsonify({}), 200
        
@app_views.route("/mechanics/<mechanic_id>/reviews", \
                 methods=["GET", "POST"], strict_slashes=False)
@app_views.route("/mechanics/<mechanic_id>/reviews/<review_id>", \
                 methods=["GET", "POST", "DELETE"], strict_slashes=False)
def mech_reviews(mechanic_id=None, review_id=None):
    if not mechanic_id:
        abort(400)
    mech_obj = storage.get(Mechanic, mechanic_id)
    if not mech_obj:
        abort(404)
    if not review_id:
        if request.method == "GET":
            all_reviews = storage.all(Review)
            mech_reviews = [one_review.to_dict() for one_review in \
                            all_reviews if one_review.id == mechanic_id]
            return jsonify(mech_reviews), 200
        if request.method == "POST":
            review_dict = request.get_json()
            if not review_dict or type(review_dict) is not dict:
                abort(400, "Invalid input")
            if review_dict.get("client_id") is None \
                or review_dict.get("description") is None \
                    or review_dict.get("rating") is None:
                abort(400, "Incomplete information")
            review_dict["mechanic_id"] = mechanic_id
            review_obj = Review(**review_dict)
            return jsonify(review_obj.to_dict()), 200
        
        if review_id:
            review_obj = storage.get(Review, review_id)
            if not review_obj:
                abort(404)
            if request.method == "GET":
                return jsonify(review_obj.to_dict()), 200
            if request.method == "PUT":
                review_attr = request.get_json()
                if not review_attr or type(review_attr) is not dict:
                    abort(400, "Invalid input")
                for key, value in review_attr.items():
                    setattr(review_obj, key, value)
                review_obj.save()
                return jsonify(review_obj.to_dict()), 201
            if request.method == "DELETE":
                review_obj.delete()
                storage.save()
                return jsonify({}), 200