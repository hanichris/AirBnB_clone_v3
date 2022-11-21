#!/usr/bin/python3
""" Module to define blueprint view for State objects """

from api.v1.views.__init__ import app_views
from api.v1.app import get_storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, request, abort, make_response
from uuid import uuid4


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET", "POST"], strict_slashes=False)
def reviews(place_id):
    """ Returns or creates Reviews objects belonging to a Place from given id
    """
    storage = get_storage()
    list_objects = []
    new_list_objects = []
    try:
        if storage is None or not isinstance(
                place_id, str) or storage.get(Place, place_id) is None:
            abort(404)
        if request.method == "GET":
            list_objects.extend(storage.all(Place).values())
            if len(list_objects) == 0:
                abort(404)
            for obj in list_objects:
                if obj.to_dict().get("place_id") == place_id:
                    new_list_objects.append(obj.to_dict())
            return jsonify(new_list_objects)
        elif request.method == "POST":
            if not request.is_json:
                abort(make_response(jsonify({"error": "Not a JSON"}), 400))
            req = request.get_json()
            if req.get("user_id") is None:
                abort(make_response(
                    jsonify({"error": "Missing user_id"}), 400))
            if storage.get(User, req.get("user_id")) is None:
                abort(404)
            if req.get("text") is None:
                abort(make_response(
                    jsonify({"error": "Missing text"}), 400))
            if req.get("id") is None:
                review_id = str(uuid4())
                req.update({"id": review_id})
            else:
                review_id = req.get("id")
            req.update({"place_id": place_id})
            storage.new(Review(**req))
            storage.save()
            return jsonify(storage.get(Review, review_id).to_dict()), 201
    except BaseException:
        raise


@app_views.route("/reviews/<review_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_reviews(review_id):
    """ Performs the operation from method on the Review from given Review id
    """
    storage = get_storage()
    try:
        if storage is None or not isinstance(
                review_id, str) or storage.get(Review, review_id) is None:
            abort(404)
        city_object = storage.get(Review, review_id)
        if city_object is None or not isinstance(review_id, str):
            raise
        if request.method == "GET":
            return jsonify(city_object.to_dict())
        elif request.method == "PUT":
            if not request.is_json:
                abort(make_response(jsonify({"error": "Not a JSON"}), 400))
            req = request.get_json()
            for k, v in req.items():
                if k != "id" and k != "created_at" and k != "updated_at" \
                        and k != "user_id" and k != "place_id":
                    setattr(city_object, k, v)
            storage.save()
            return jsonify(city_object.to_dict()), 200
        elif request.method == "DELETE":
            storage.delete(city_object)
            storage.save()
            return jsonify({}), 200
    except BaseException:
        raise
