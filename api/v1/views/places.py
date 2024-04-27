#!/usr/bin/python3
"""Module for users API"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places():
    """Retrieves the list of all place objects in cities"""
    city = storage.get(City, city_id)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def one_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, user_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Returns an empty dictionary with the status code 200"""
    place = storage.get(Place, user_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place():
    """Returns new Place Object"""
    if not storage.get(City, city_id):
        abort(404)

    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")
    if 'user_id' not in new_place:
        abort(400, "Missing user_id")
    if 'name' not in new_place:
        abort(400, 'Missing name')

    if not storage.get(User, new_place['user_id']):
        abort(404)

    place = Place(**new_place)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Modifies a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for key, value in req.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
