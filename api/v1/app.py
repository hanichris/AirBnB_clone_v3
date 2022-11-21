#!/usr/bin/python3
"""Start of the Flask API."""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_storage(self):
    storage.close()

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify({'error': 'Not found'}), 404

if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    app.run(
            host= HBNB_API_HOST or '0.0.0.0',
            port = HBNB_API_PORT or '5000',
            threaded=True
            )
