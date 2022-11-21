#!/usr/bin/python3
"""View for State objects.

It handles all default RESTful API actions.
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<state_id>', strict_slashes=False)
def read_states(state_id=None):
    """Retrieve the list of all State objects.

    If `state_id` is not None, retrieve the state object
    represented by that id.
    Args:
        state_id (string): state object identifier.
    """
    if state_id is None:
        states_objs = storage.all('State')
        states = []
        for states_obj in states_objs.values():
            states.append(states_obj.to_dict())
        return jsonify(states)
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(state_obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a State object."""
    state_obj = storage.get(State, state_id)
    if state_obj is not None:
        storage.delete(state_obj)
        storage.save()
        return jsonify({}), 200
    return jsonify({'error': 'Not found'}), 404


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """Create a new State."""
    response = request.get_json()
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in response:
        return jsonify({'error': 'Missing Name'}), 400
    state_obj = State(name=response['name'])
    state_obj.save()
    return jsonify(state_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Update a particular State's attribute."""
    response = request.get_json()
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        return jsonify({'error': 'Not found'}), 404
    mask = ('id', 'created_at', 'updated_at')
    filtered_dict = dict(filter(lambda x: x[0] not in mask,
                                response.items()))
    state_obj.__dict__.update(filtered_dict)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200
