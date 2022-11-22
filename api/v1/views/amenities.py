#!/usr/bin/python3
"""View for Amenity objects.

It handles all default RESTful API actions.
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def read_amenities(amenity_id=None):
    """Retrieve the list of all Amenity objects.

    If `amenity_id` is not None, retrieve the amenity object
    represented by that id.
    Args:
        state_id (string): amenity object identifier.
    """
    if amenity_id is None:
        amenity_objs = storage.all('Amenity')
        amenities = []
        for amenity_obj in amenity_objs.values():
            amenities.append(amenity_obj.to_dict())
        return jsonify(amenities)
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an Amenity object."""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is not None:
        storage.delete(amenity_obj)
        storage.save()
        return jsonify({}), 200
    return jsonify({'error': 'Not found'}), 404


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Create a new Amenity."""
    response = request.get_json()
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in response:
        return jsonify({'error': 'Missing name'}), 400
    amenity_obj = Amenity(name=response['name'])
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update a particular Amenity's attribute."""
    response = request.get_json()
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        return jsonify({'error': 'Not found'}), 404
    mask = ('id', 'created_at', 'updated_at')
    filtered_dict = dict(filter(lambda x: x[0] not in mask,
                                response.items()))
    amenity_obj.__dict__.update(filtered_dict)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200
