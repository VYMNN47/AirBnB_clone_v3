#!/usr/bin/python3
"""Module for places API"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """Retrieves the list of all place objects in cities"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def one_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Returns an empty dictionary"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Returns new Place Object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")
    if 'user_id' not in new_place:
        abort(400, "Missing user_id")
    user = storage.get(User, new_place['user_id'])
    if not user:
        abort(404)
    if 'name' not in new_place:
        abort(400, 'Missing name')

    place = Place(**new_place)
    setattr(place, 'city_id', city_id)
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
