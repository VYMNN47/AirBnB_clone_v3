#!/usr/bin/python3
"""Module for reivews API"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
import os


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def place_amenities(place_id):
    """Retrieves the list of all review objects in places"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Returns an empty dictionary"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids

    if amenity not in amenities:
        abort(404)
    amenities.remove(amenity)
    place.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """Returns new Review Object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids

    if amenity in amenities:
        return jsonify(amenity.to_dict), 200

    amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
