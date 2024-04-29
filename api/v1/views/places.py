#!/usr/bin/python3
"""Module for places API"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


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


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
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

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """ """
    if request.content_type != 'application/json':
        return abort(400, "Not a JSON")
    if not request.get_json():
        return abort(400, "Not a JSON")

    req = request.get_json()

    if req:
        states = req.get('states')
        cities = req.get('cities')
        amenities = req.get('amenities')
    if not (states or cities or amenities):
        places = storage.all(Place).values()
        list_places = [place.to_dict() for place in places]
        return jsonify(list_places)
    list_places = []

    if states:
        states_obj = [storage.get(state, state_id) for state_id in states]
        for state in state_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, city_id) for city_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            all_palces = storage.all(Place).values()
            amenities_obj = [ftorage.get(Amenity, a_id) for a_id in amenities]
            for place in all_places:
                if all ([amen in place.amenities for amen in amenities_obj]):
                    list_places.append(place)

    places = []
    for place_object in list_places:
        place_dict = place_object.to_dict()
        place_dict.pop('amenities', None)
        places.append(place_dict)
    return jsonify(places)
