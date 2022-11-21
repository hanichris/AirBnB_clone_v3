#!/usr/bin/python3
""" Module to define blueprint view for State objects """

from api.v1.views.__init__ import app_views
from api.v1.app import get_storage
from models.state import State
from flask import jsonify, request, abort, make_response
from uuid import uuid4


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def states():
    """ Returns State objects """
    storage = get_storage()
    list_objects = []
    new_list_objects = []
    try:
        if storage is not None:
            if request.method == "GET":
                list_objects.extend(storage.all(State).values())
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
                if req.get("id") is None:
                    state_id = str(uuid4())
                    req.update({"id": state_id})
                else:
                    state_id = req.get("id")
                storage.new(State(**req))
                storage.save()
                return jsonify(storage.get(State, state_id).to_dict()), 201
    except BaseException:
        raise


@app_views.route("/states/<state_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_state(state_id):
    """ Performs the operation from method on the state from given state id """
    storage = get_storage()
    try:
        if storage is not None:
            state_object = storage.get(State, state_id)
            if state_object is None or not isinstance(state_id, str):
                raise
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
