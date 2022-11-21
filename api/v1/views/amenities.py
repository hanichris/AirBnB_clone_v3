#!/usr/bin/python3
""" Module to define blueprint view for State objects """

from api.v1.views.__init__ import app_views
from api.v1.app import get_storage
from models.amenity import Amenity
from flask import jsonify, request, abort, make_response
from uuid import uuid4


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
def list_amenities():
    """ Returns all Amenity objects """
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
            if req.get("id") is None:
                amenity_id = str(uuid4())
                req.update({"id": amenity_id})
            else:
                amenity_id = req.get("id")
            storage.new(Amenity(**req))
            storage.save()
            return jsonify(storage.get(Amenity, amenity_id).to_dict()), 201
    except BaseException:
        raise


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET", "POST", "PUT", "DELETE"], strict_slashes=False)
def amenities(amenity_id):
    """ Performs the operation from method on the Amenity from given id """
    storage = get_storage()
    list_objects = []
    new_list_objects = []
    try:
        if storage is None or not isinstance(
                amenity_id, str) or storage.get(Amenity, amenity_id) is None:
            abort(404)
        amenity_object = storage.get(Amenity, amenity_id)
        if amenity_object is None:
            raise
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
