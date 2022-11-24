#!/usr/bin/python3
""" Module to define blueprint view for Amenity objects """

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.amenity import Amenity
from flask import jsonify, request, abort, make_response


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
def list_amenities():
    """
        Returns all Amenity objects for `GET` requests,
        or the created Amenity object for `POST` requests,
        otherwise raises an exception.
    """
    storage = get_storage()
    list_objects = []
    new_list_objects = []
    try:
        if storage is None:
            abort(404)
        if request.method == "GET":
            list_objects.extend(storage.all(Amenity).values())
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
            amenity_obj = Amenity(**req)
            storage.new(amenity_obj)
            storage.save()
            return jsonify(amenity_obj.to_dict()), 201
    except BaseException:
        raise


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET", "POST", "PUT", "DELETE"], strict_slashes=False)
def amenities(amenity_id):
    """
    Args:
        amenity_id (string): Amenity object identifier.

    Returns:
        A dictionary represenatation of the Amenity object
        with the given id for `GET` requests,
        or the updated Amenity object with the given id for `PUT` requests,
        or an empty dictionary for `DELETE` requests,
        otherwise raises an exception.

    """
    storage = get_storage()
    try:
        if storage is None or not isinstance(amenity_id, str) \
                or storage.get(Amenity, amenity_id) is None:
            abort(404)
        amenity_object = storage.get(Amenity, amenity_id)
        if request.method == "GET":
            return jsonify(amenity_object.to_dict())
        elif request.method == "PUT":
            if not request.is_json:
                abort(make_response(jsonify({"error": "Not a JSON"}), 400))
            req = request.get_json()
            for k, v in req.items():
                if k != "id" and k != "created_at" and k != "updated_at":
                    setattr(amenity_object, k, v)
            storage.save()
            return jsonify(amenity_object.to_dict()), 200
        elif request.method == "DELETE":
            storage.delete(amenity_object)
            storage.save()
            return jsonify({}), 200
    except BaseException:
        raise
