#!/usr/bin/python3
"""View for User objects.

It handles all default RESTful API actions.
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
@app_views.route('/users/<user_id>', strict_slashes=False)
def read_users(user_id=None):
    """Retrieve the list of all User objects.

    If `user_id` is not None, retrieve the user object
    represented by that id.
    Args:
        user_id (string): user object identifier.
    """
    if user_id is None:
        users_objs = storage.all('User')
        users = []
        for users_obj in users_objs.values():
            users.append(users_obj.to_dict())
        return jsonify(users)
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete a User object."""
    user_obj = storage.get(User, user_id)
    if user_obj is not None:
        storage.delete(user_obj)
        storage.save()
        return jsonify({}), 200
    return jsonify({'error': 'Not found'}), 404


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Create a new User."""
    response = request.get_json()
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in response:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in response:
        return jsonify({'error': 'Missing password'}), 400
    user_obj = User(**response)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Update a particular User's attribute."""
    response = request.get_json()
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        return jsonify({'error': 'Not found'}), 404
    mask = ('id', 'email', 'created_at', 'updated_at')
    filtered_dict = dict(filter(lambda x: x[0] not in mask,
                                response.items()))
    user_obj.__dict__.update(filtered_dict)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
