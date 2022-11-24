#!/usr/bin/python3
"""View for State objects.

It handles all default RESTful API actions.
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State
from flask import jsonify, request, abort, make_response


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def states():
    """
        Returns all State objects for `GET` requests,
        or the created State object for `POST` requests,
        otherwise raises an exception.
    """
    storage = get_storage()
    list_objects = []
    new_list_objects = []
    try:
        if storage is None:
            abort(404)
        if request.method == "GET":
            list_objects.extend(storage.all(State).values())
            if len(list_objects) == 0:
                abort(404)
            for obj in list_objects:
                new_list_objects.append(obj.to_dict())
            return jsonify(new_list_objects)
        elif request.method == "POST":
            if not request.is_json:
                abort(make_response(jsonify({"error": "Not a JSON"}), 400))
            req = request.get_json()
            if req.get("name") is None:
                abort(make_response(
                    jsonify({"error": "Missing name"}), 400))
            state_obj = State(**req)
            storage.new(state_obj)
            storage.save()
            return jsonify(state_obj.to_dict()), 201
    except BaseException:
        raise


@app_views.route("/states/<state_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_state(state_id):
    """
    Args:
        state_id (string): State object identifier.

    Returns:
        A dictionary represenatation of the State object
        with the given id for `GET` requests,
        or the updated State object with the given id for `PUT` requests,
        or an empty dictionary for `DELETE` requests,
        otherwise raises an exception.

    """
    storage = get_storage()
    try:
        if storage is None or not isinstance(state_id, str) \
                or storage.get(State, state_id) is None:
            abort(404)
        state_object = storage.get(State, state_id)
        if request.method == "GET":
            return jsonify(state_object.to_dict())
        elif request.method == "PUT":
            if not request.is_json:
                abort(make_response(jsonify({"error": "Not a JSON"}), 400))
            req = request.get_json()
            for k, v in req.items():
                if k != "id" and k != "created_at" and k != "updated_at":
                    setattr(state_object, k, v)
            storage.save()
            return jsonify(state_object.to_dict()), 200
        elif request.method == "DELETE":
            storage.delete(state_object)
            storage.save()
            return jsonify({}), 200
    except BaseException:
        raise
