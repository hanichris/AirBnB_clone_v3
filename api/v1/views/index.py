#!/usr/bin/python3
""" Module to create flask views for index page """

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from api.v1.views.__init__ import app_views
from api.v1.app import g, get_storage
from flask import jsonify

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route("/", strict_slashes=False)
def root():
    """ Returns the root page """
    return jsonify({})


@app_views.route("/status", strict_slashes=False)
def status():
    """ Returns the status page """
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """ Returns the stats page """
    if "storage" in g:
        storage = g.pop("storage", None)
    else:
        storage = get_storage()
    class_stats = {}
    if storage is not None:
        for key, _cls in classes.items():
            class_stats.update({key: storage.count(_cls)})
    return jsonify(class_stats)
