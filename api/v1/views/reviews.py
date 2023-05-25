#usr/bin/python3

from api.v1.views import app_views
from models import storage
from models.review import Review
from flask import request, jsonify

@app_views.route("/reviews", methods=["GET", "POST"], strict_slashes=False)
@app_views.route("/reviews/<review_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_all_reviews(review_id=None):
    all_reviews = storage.all(Review).values()

    review_list = [review.to_dict() for review in all_reviews]

    if not review_id:
        if request.method == "GET":
            return jsonify(review_list), 200
        
