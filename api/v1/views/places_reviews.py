#!/usr/bin/python3
"""View for Place objects.

It handles all default RESTful API actions.
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def read_places(city_id):
    """Retrieve the list of all Place objects.

    The Place objects are of a particular city identified by
    the city id.
    Args:
        city_id (string): city object identifier.
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        return jsonify({'error': 'Not found'}), 404
    places = []
    for place in city_obj.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def read_place(place_id):
    """Retrieve the place identified by the given id."""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object."""
    place_obj = storage.get(Place, place_id)
    if place_obj is not None:
        storage.delete(place_obj)
        storage.save()
        return jsonify({}), 200
    return jsonify({'error': 'Not found'}), 404


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a new Place."""
    response = request.get_json()
    city_obj = storage.get(City, city_id)
    user_obj = storage.get(User, response['user_id'])
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in response:
        return jsonify({'error': 'Missing name'}), 400
    if 'user_id' not in response:
        return jsonify({'error': 'Missing user_id'}), 400
    if city_obj is None:
        return jsonify({'error': 'Not found'}), 404
    if user_obj is None:
        return jsonify({'error': 'Not found'}), 404
    response['city_id'] = city_id
    place_obj = Place(**response)
    place_obj.save()
    return jsonify(place_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Update a particular Place's attribute."""
    response = request.get_json()
    place_obj = storage.get(Place, place_id)
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if place_obj is None:
        return jsonify({'error': 'Not found'}), 404
    mask = ('id', 'user_id', 'city_id', 'created_at', 'updated_at')
    filtered_dict = dict(filter(lambda x: x[0] not in mask,
                                response.items()))
    place_obj.__dict__.update(filtered_dict)
    place_obj.save()
    return jsonify(place_obj.to_dict()), 200
