import profile
from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token
from api.models.db import db
from api.models.review import Review

reviews = Blueprint('reviews', 'reviews')

@reviews.route('/', methods=['POST'])
@login_required
def create():
  data = request.get_json()
  profile = read_token(request)
  data['profile_id'] = profile['id']
  review = Review(**data)
  db.session.add(review)
  db.session.commit()
  return jsonify(review.serialize()), 201 


@reviews.route('/<id>/edit', methods=['PUT'])
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  review = Review.query.filter_by(id=id).first()

  if review.profile_id != profile["id"]:
    return "forbidden", 403
  
  for key in data:
    setattr(review, key, data[key])

  db.session.commit()
  return jsonify(review.serialize()), 200


@reviews.route('/index', methods=['GET'])
@login_required
def index():
  reviews = Review.query.all()
  return jsonify([review.serialize() for review in reviews]), 200


@reviews.route('/<id>', methods=["GET"])
@login_required
def show(id):
  review = Review.query.filter_by(id=id).first()
  return jsonify(review.serialize()), 200


@reviews.route('/<id>', methods=['DELETE'])
@login_required
def delete(id):
  profile = read_token(request)
  review = Review.query.filter_by(id=id).first()

  if review.profile_id != profile["id"]:
    return "forbidden", 403
  
  db.session.delete(review)
  db.session.commit()
  return jsonify(message="Success"), 208