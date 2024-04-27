#!/usr/bin/python3
"""Handles State API actions"""
from api.v1.views import app_views
from json import dumps
from flask import abort, jsonify, request, make_response, Response
from models import storage
from models.city import City


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def state():
    """Retrieves the list of all State objects"""
    objs = storage.all("City")
    data = [obj.to_dict() for obj in objs.values()]
    return Response(response=dumps(data, indent=2)
                    + '\n', mimetype='application/json')


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def one_state(city_id):
    """Retrieves a State object"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    data = obj.to_dict()
    return Response(response=dumps(data, indent=2)
                    + '\n', mimetype='application/json')


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(city_id):
    """Deletes a State object"""
    city = storage.get(City, city_id)
    if state is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def new_state():
    """Creates a new State"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    else:
        obj = City(**request.get_json())
        obj.save()
        data = obj.to_dict()
        return Response(response=dumps(data, indent=2)
                        + '\n', mimetype='application/json'), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(city_id):
    """Updates an exisiting State Object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    city_data = request.get_json()
    city.name = city_data['name']
    city.save()
    data = city.to_dict()
    return Response(response=dumps(data, indent=2)
                    + '\n', mimetype='application/json')
