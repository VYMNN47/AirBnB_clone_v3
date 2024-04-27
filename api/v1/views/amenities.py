#!/usr/bin/python3
"""Handles the states API."""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenity():
    """Returns list of all Amenity objects"""
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def single_amenity(amenity_id):
    """Returns a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenity/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a new state object"""
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if 'name' not in new_amenity:
        abort(400, "Missing name")
    amenity = Amenity(**new_amenity)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(amenity_id):
    """Updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for key, value in req.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
