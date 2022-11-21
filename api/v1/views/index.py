#!/usr/bin/python3
"""Status of api."""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {'Amenity': Amenity,
           'City': City,
           'Place': Place,
           'Review': Review,
           'State': State,
           'User': User
           }


@app_views.route('/status', strict_slashes=False)
def status():
    """return status."""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Retrieve count of each object by type."""
    results = {}
    for cls in classes.values():
        count = storage.count(cls)
        results[cls.__name__.lower()] = count
    return jsonify(results)
