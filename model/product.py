from datetime import datetime

from database import db


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    stock = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    # order_details = db.relationship("OrderDetail", backref="order")

    def decrease_stock(self, count):
        self.stock -= count