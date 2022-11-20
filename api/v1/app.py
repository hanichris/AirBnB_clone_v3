#!/usr/bin/python3
""" Module to create a flask server """

from flask import Flask, g, jsonify, json
from models import storage
from api.v1.views import app_views
from os import getenv
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv("HBNB_API_HOST", "0.0.0.0")
port = getenv("HBNB_API_PORT", "5000")


def get_storage():
    """ Creates a resource for the storage engine """
    if "storage" not in g:
        g.storage = storage
    return g.storage


@app.teardown_appcontext
def teardown_storage(exception):
    """ Deallocates the resource used as storage engine """
    _storage = g.pop("storage", None)
    if _storage is not None:
        _storage.close()


@app.errorhandler(Exception)
def handle_errors(e: Exception):
    """ Returns JSON instead of HTML error page on any kind of error """
    if isinstance(e, HTTPException):
        return jsonify({"error": "Not found"}), e.code
    response = e.get_response()
    response.data = json.dump({
        "code": e.code,
        "name": e.name,
        "description": e.description
    })
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True, debug=True)
