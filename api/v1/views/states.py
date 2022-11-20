#!/usr/bin/python3
""" Module to define blueprint view for State objects """

from api.v1.views.__init__ import app_views
from api.v1.app import g, get_storage
from models.state import State
from flask import jsonify, request, abort


@app_views.route("/states", strict_slashes=False)
def states():
    """ Returns State objects """
    if "storage" in g:
        storage = g.pop("storage", None)
    else:
        storage = get_storage()
    list_objects = []
    new_list_objects = []
    if storage is not None:
        list_objects.extend(storage.all(State).values())
        for obj in list_objects:
            new_list_objects.append(obj.to_dict())
    return jsonify(new_list_objects)


@app_views.route("/states/<state_id>",
                 methods=["GET", "POST", "PUT", "DELETE"], strict_slashes=False)
def get_state(state_id):
    """ Performs the operation from method on the state from given state id """
    if "storage" in g:
        storage = g.pop("storage", None)
    else:
        storage = get_storage()
    try:
        if request.method == "GET":
            state_object = storage.get(State, int(state_id))
            if not isinstance(int(state_id), int) or state_object is None:
                raise
            return jsonify(state_object.to_dict())
        elif request.method == "DELETE":
            state_object = storage.get(State, int(state_id))
            if not isinstance(int(state_id), int) or state_object is None:
                raise
            storage.delete(state_object)
            return jsonify({}), 200
        elif request.method == "POST":
            req = request.get_json()
            if req is None:
                raise
            if not isinstance(req, dict):
                abort(jsonify({"error": "Not a JSON"}), 404)
            if req.get("name") is None:
                abort(jsonify({"error": "Missing name"}), 404)
            storage.new(State(**req))
            storage.save()
            return jsonify(storage.get(State, state_id).to_dict()), 201
        elif request.method == "PUT":
            if not isinstance(int(state_id), int) or state_object is None:
                raise
            req = request.get_json()
            if req is None:
                raise
            if not isinstance(req, dict):
                abort(jsonify({"error": "Not a JSON"}), 404)
            state_object = storage.get(State, state_id)
            state_dict = {}
            if state_object is None:
                raise
            for k, v in req:
                if k != "id" and k != "created_at" and k != "updated_at":
                    state_dict.update({k, v})
            state_object.__dict__.update(state_dict)
            storage.save()
            return jsonify(state_object.to_dict()), 200
    except BaseException:
        abort(404)
