#!/usr/bin/python3
"""This module contains the Flask application for the API."""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.errorhandler(404)
def error_404(error):
    """Returns Not Found on 404"""
    data = {'error': 'Not found'}
    return Response(response=dumps(data, indent=2)
                    + '\n', mimetype='application/json')


@app.teardown_appcontext
def close_storage(exception):
    """Handles closing Storage"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
