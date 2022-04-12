from datetime import datetime
from api.models.db import db

class Review(db.Model):
  __tablename__ = 'reviews'
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  text = db.Column(db.Text, nullable=False)
  art_id = db.Column(db.Integer)
  rating = db.Column(db.Integer)
  profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

  def __init__(self, text, user_id, rating, art_id, profile_id):
    self.text = text
    self.user_id = user_id
    self.rating = rating
    self.art_id = art_id
    self.profile_id = profile_id

  def __repr__(self):
    return f"Post ID: {self.id} -- Date: {self.date}"

  def serialize(self):
    review = {c.name: getattr(self, c.name) for c in self.__table__.columns}
    return review