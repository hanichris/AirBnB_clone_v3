#!/usr/bin/python3
"""View for City objects.

It handles all default RESTful API actions.
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def read_cities(state_id):
    """Retrieve the list of all City objects.

    The City objects are of a particular state identified by
    the state id.
    Args:
        state_id (string): state object identifier.
    """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        return jsonify({'error': 'Not found'}), 404
    cities = []
    for city in state_obj.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def read_city(city_id):
    """Retrieve the city identified by the given id."""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete a City object."""
    city_obj = storage.get(City, city_id)
    if city_obj is not None:
        storage.delete(city_obj)
        storage.save()
        return jsonify({}), 200
    return jsonify({'error': 'Not found'}), 404


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a new City."""
    response = request.get_json()
    state_obj = storage.get(State, state_id)
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in response:
        return jsonify({'error': 'Missing name'}), 400
    if state_obj is None:
        return jsonify({'error': 'Not found'}), 404
    response['state_id'] = state_id
    city_obj = City(**response)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Update a particular City's attribute."""
    response = request.get_json()
    city_obj = storage.get(City, city_id)
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if city_obj is None:
        return jsonify({'error': 'Not found'}), 404
    mask = ('id', 'state_id', 'created_at', 'updated_at')
    filtered_dict = dict(filter(lambda x: x[0] not in mask,
                                response.items()))
    city_obj.__dict__.update(filtered_dict)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
