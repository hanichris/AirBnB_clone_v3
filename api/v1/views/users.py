#!/usr/bin/python3
""" Module to define blueprint view for User objects """

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.user import User
from flask import jsonify, request, abort, make_response


@app_views.route("/users",
                 methods=["GET", "POST"], strict_slashes=False)
def users():
    """
        Returns all User objects for `GET` requests,
        or the created User object for `POST` requests,
        otherwise raises an exception.
    """
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
            user_obj = User(**req)
            storage.new(user_obj)
            storage.save()
            return jsonify(user_obj.to_dict()), 201
    except BaseException:
        raise


@app_views.route("/users/<user_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_user(user_id):
    """
    Args:
        user_id (string): User object identifier.

    Returns:
        A dictionary represenatation of the User object
        with the given id for `GET` requests,
        or the updated User object with the given id for `PUT` requests,
        or an empty dictionary for `DELETE` requests,
        otherwise raises an exception.

    """
    storage = get_storage()
    try:
        if storage is None or not isinstance(user_id, str) \
                or storage.get(User, user_id) is None:
            abort(404)
        user_object = storage.get(User, user_id)
        if request.method == "GET":
            return jsonify(user_object.to_dict())
        elif request.method == "PUT":
            if not request.is_json:
                abort(make_response(jsonify({"error": "Not a JSON"}), 400))
            req = request.get_json()
            for k, v in req.items():
                if k != "id" and k != "created_at" and k != "updated_at" \
                        and k != "email":
                    setattr(user_object, k, v)
            storage.save()
            return jsonify(user_object.to_dict()), 200
        elif request.method == "DELETE":
            storage.delete(user_object)
            storage.save()
            return jsonify({}), 200
    except BaseException:
        raise
