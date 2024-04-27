#!/usr/bin/python3
"""Handles State API actions"""
from api.v1.views import app_views
from json import dumps
from flask import abort, jsonify, request, make_response, Response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state():
    """Retrieves the list of all State objects"""
    objs = storage.all("State")
    data = [obj.to_dict() for obj in objs.values()]
#    return jsonify([obj.to_dict() for obj in objs.values()])
    return Response(response=dumps(data, indent=2)
                    + '\n', mimetype='application/json')


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def one_state(state_id):
    """Retrieves a State object"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    data = obj.to_dict()
    return Response(response=dumps(data, indent=2)
                    + '\n', mimetype='application/json')


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def new_state():
    """Creates a new State"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    else:
        obj = State(**request.get_json())
        obj.save()
        data = obj.to_dict()
        return Response(response=dumps(data, indent=2)
                        + '\n', mimetype='application/json'), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Updates an exisiting State Object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    state_data = request.get_json()
    state.name = state_data['name']
    state.save()
    data = state.to_dict()
    return Response(response=dumps(data, indent=2)
                    + '\n', mimetype='application/json')
