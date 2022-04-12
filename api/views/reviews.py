from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token
from api.models.db import db
from api.models.review import Review

reviews = Blueprint('reviews', 'reviews')

@reviews.route('/', methods=['POST'])
@login_required
def create():
  print('------> createReview <-----')
  data = request.get_json()
  profile = read_token(request)
  data['profile_id'] = profile['id']
  review = Review(**data)
  db.session.add(review)
  db.session.commit()
  print(f'@@@ view: review @@@@ ',review)
  return jsonify(review.serialize()), 201 