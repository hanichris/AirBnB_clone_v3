#!/usr/bin/python3
""" Module to define blueprint view for State objects """

from api.v1.views.__init__ import app_views
from api.v1.app import get_storage
from models.city import City
from models.state import State
from flask import jsonify, request, abort, make_response
from uuid import uuid4


@app_views.route("/states/<state_id>/cities",
                 methods=["GET", "POST"], strict_slashes=False)
def cities(state_id):
    """ Returns or creates City objects belonging to a State from given id """
    storage = get_storage()
    list_objects = []
    new_list_objects = []
    try:
        if storage is None or not isinstance(
                state_id, str) or storage.get(State, state_id) is None:
            abort(404)
        if request.method == "GET":
            list_objects.extend(storage.all(City).values())
            if len(list_objects) == 0:
                abort(404)
            for obj in list_objects:
                if obj.to_dict().get("state_id") == state_id:
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
                city_id = str(uuid4())
                req.update({"id": city_id})
            else:
                city_id = req.get("id")
            req.update({"state_id": state_id})
            storage.new(City(**req))
            storage.save()
            return jsonify(storage.get(City, city_id).to_dict()), 201
    except BaseException:
        raise


@app_views.route("/cities/<city_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_city(city_id):
    """ Performs the operation from method on the City from given City id """
    storage = get_storage()
    try:
        if storage is None or not isinstance(
                city_id, str) or storage.get(City, city_id) is None:
            abort(404)
        city_object = storage.get(City, city_id)
        if city_object is None or not isinstance(city_id, str):
            raise
        if request.method == "GET":
            return jsonify(city_object.to_dict())
        elif request.method == "PUT":
            if not request.is_json:
                abort(make_response(jsonify({"error": "Not a JSON"}), 400))
            req = request.get_json()
            for k, v in req.items():
                if k != "id" and k != "created_at" and k != "updated_at" and k != "state_id":
                    setattr(city_object, k, v)
            storage.save()
            return jsonify(city_object.to_dict()), 200
        elif request.method == "DELETE":
            storage.delete(city_object)
            storage.save()
            return jsonify({}), 200
    except BaseException:
        raise
