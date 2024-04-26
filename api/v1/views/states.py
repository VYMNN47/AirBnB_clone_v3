#!/usr/bin/python3

from flask import abort, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def state():
    """Retrieves the list of all State objects"""
    objs = storage.all(State)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route('/states/<state_id>', methods=['GET'])
def one_state(state_id):
    """Retrieves a State object"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)



