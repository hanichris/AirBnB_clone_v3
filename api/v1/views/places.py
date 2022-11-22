#!/usr/bin/python3
"""View for Review objects.

It handles all default RESTful API actions.
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def read_reviews(place_id):
    """Retrieve the list of all Review objects.

    The Review objects are of a particular place identified by
    the place id.
    Args:
        place_id (string): place object identifier.
    """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        return jsonify({'error': 'Not found'}), 404
    reviews = []
    for review in place_obj.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def read_review(review_id):
    """Retrieve the review identified by the given id."""
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object."""
    review_obj = storage.get(Review, review_id)
    if review_obj is not None:
        storage.delete(review_obj)
        storage.save()
        return jsonify({}), 200
    return jsonify({'error': 'Not found'}), 404


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a new Review."""
    response = request.get_json()
    place_obj = storage.get(Place, place_id)
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in response:
        return jsonify({'error': 'Missing user_id'}), 400
    if 'text' not in response:
        return jsonify({'error': 'Missing text'}), 400
    if place_obj is None:
        return jsonify({'error': 'Not found'}), 404
    response['place_id'] = place_id
    review_obj = Review(**response)
    review_obj.save()
    return jsonify(review_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update a particular Review's attribute."""
    response = request.get_json()
    review_obj = storage.get(Review, review_id)
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if review_obj is None:
        return jsonify({'error': 'Not found'}), 404
    mask = ('id', 'user_id', 'place_id', 'created_at', 'updated_at')
    filtered_dict = dict(filter(lambda x: x[0] not in mask,
                                response.items()))
    review_obj.__dict__.update(filtered_dict)
    review_obj.save()
    return jsonify(review_obj.to_dict()), 200
