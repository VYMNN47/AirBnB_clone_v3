#!/usr/bin/python3
"""Routes API"""
from api.v1.views import app_views
from flask import Response
from json import dumps
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Returns the status: OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Returns the stats of storage entities"""
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return Response(response=dumps(data, indent=2)
                    + '\n', mimetype='application/json')
