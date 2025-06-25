from datetime import datetime

from database import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    orders = db.relationship("Order")