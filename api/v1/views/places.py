#!/usr/bin/python3
""" Module to define blueprint view for Place objects """

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, request, abort, make_response


@app_views.route("/cities/<city_id>/places",
                 methods=["GET", "POST"], strict_slashes=False)
def places(city_id):
    """
    Args:
        city_id (string): City object identifier.

    Returns:
        A list of all Place objects with given City id for `GET` requests,
        or the created Place object for a given City id in `POST` requests,
        otherwise raises an exception.

    """
    storage = get_storage()
    list_objects = []
    new_list_objects = []
    try:
        if storage is None or not isinstance(
                city_id, str) or storage.get(City, city_id) is None:
            abort(404)
        if request.method == "GET":
            list_objects.extend(storage.all(Place).values())
            if len(list_objects) == 0:
                abort(404)
            for obj in list_objects:
                if obj.to_dict().get("city_id") == city_id:
                    new_list_objects.append(obj.to_dict())
            return jsonify(new_list_objects)
        elif request.method == "POST":
            if not request.is_json:
                abort(make_response(jsonify({"error": "Not a JSON"}), 400))
            req = request.get_json()
            if req.get("name") is None:
                abort(make_response(
                    jsonify({"error": "Missing name"}), 400))
            if req.get("user_id") is None:
                abort(make_response(
                    jsonify({"error": "Missing user_id"}), 400))
            if storage.get(User, req.get("user_id")) is None:
                abort(404)
            req.update({"city_id": city_id})
            place_obj = Place(**req)
            storage.new(place_obj)
            storage.save()
            return jsonify(place_obj.to_dict()), 201
    except BaseException:
        raise


@app_views.route("/places/<place_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_place(place_id):
    """
    Args:
        place_id (string): Place object identifier.

    Returns:
        A dictionary represenatation of the Place object
        with the given id for `GET` requests,
        or the updated Place object with the given id for `PUT` requests,
        or an empty dictionary for `DELETE` requests,
        otherwise raises an exception.

    """
    storage = get_storage()
    try:
        if storage is None or not isinstance(place_id, str) \
                or storage.get(Place, place_id) is None:
            abort(404)
        place_object = storage.get(Place, place_id)
        if request.method == "GET":
            return jsonify(place_object.to_dict())
        elif request.method == "PUT":
            if not request.is_json:
                abort(make_response(jsonify({"error": "Not a JSON"}), 400))
            req = request.get_json()
            for k, v in req.items():
                if k != "id" and k != "created_at" and k != "updated_at" \
                        and k != "user_id" and k != "city_id":
                    setattr(place_object, k, v)
            storage.save()
            return jsonify(place_object.to_dict()), 200
        elif request.method == "DELETE":
            storage.delete(place_object)
            storage.save()
            return jsonify({}), 200
    except BaseException:
        raise
