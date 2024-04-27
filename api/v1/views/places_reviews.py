#!/usr/bin/python3
"""Module for places API"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews(place_id):
    """Retrieves the list of all place objects in cities"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def one_review(review_id):
    """Retrieves a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Returns an empty dictionary"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Returns new Review Object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    new_review = request.get_json()
    if not new_review:
        abort(400, "Not a JSON")
    if 'user_id' not in new_review:
        abort(400, "Missing user_id")
    user = storage.get(User, new_review['user_id'])
    if not user:
        abort(404)
    if 'text' not in new_review:
        abort(400, 'Missing text')

    review = Review(**new_review)
    setattr(review, 'place_id', place_id)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Modifies a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for key, value in req.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)

    review.save()
    return jsonify(place.to_dict()), 200
