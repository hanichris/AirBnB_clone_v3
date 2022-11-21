#!/usr/bin/python3
""" Module to define blueprint view for State objects """

from api.v1.views.__init__ import app_views
from api.v1.app import get_storage
from models.user import User
from flask import jsonify, request, abort, make_response
from uuid import uuid4


@app_views.route("/users",
                 methods=["GET", "POST"], strict_slashes=False)
def users():
    """ Returns or creates User objects belonging from given id """
    storage = get_storage()
    list_objects = []
    new_list_objects = []
    try:
        if storage is None:
            abort(404)
        if request.method == "GET":
            list_objects.extend(storage.all(User).values())
            if len(list_objects) == 0:
                abort(404)
            for obj in list_objects:
                new_list_objects.append(obj.to_dict())
            return jsonify(new_list_objects)
        elif request.method == "POST":
            if not request.is_json:
                abort(make_response(jsonify({"error": "Not a JSON"}), 400))
            req = request.get_json()
            if req.get("email") is None or req.get("password") is None:
                abort(make_response(
                    jsonify({"error": "Missing name"}), 400))
            if req.get("id") is None:
                user_id = str(uuid4())
                req.update({"id": user_id})
            else:
                user_id = req.get("id")
            storage.new(User(**req))
            storage.save()
            return jsonify(storage.get(User, user_id).to_dict()), 201
    except BaseException:
        raise


@app_views.route("/users/<user_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_user(user_id):
    """ Performs the operation from method on the User from given User id """
    storage = get_storage()
    try:
        if storage is None or not isinstance(
                user_id, str) or storage.get(User, user_id) is None:
            abort(404)
        user_object = storage.get(User, user_id)
        if user_object is None or not isinstance(user_id, str):
            raise
        if request.method == "GET":
            return jsonify(user_object.to_dict())
        elif request.method == "PUT":
            if not request.is_json:
                abort(make_response(jsonify({"error": "Not a JSON"}), 400))
            req = request.get_json()
            for k, v in req.items():
                if k != "id" and k != "created_at" and k != "updated_at" and k != "email":
                    setattr(user_object, k, v)
            storage.save()
            return jsonify(user_object.to_dict()), 200
        elif request.method == "DELETE":
            storage.delete(user_object)
            storage.save()
            return jsonify({}), 200
    except BaseException:
        raise
