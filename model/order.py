from datetime import datetime

from sqlalchemy import Enum

from database import db
from model.product import Product
from model.user import User


class OrderStatus(Enum):
    ready = "ready"
    complete = "complete"
    refund = "refund"
    cancel = "cancel"


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    address = db.Column(db.String)
    status = db.Column(OrderStatus, default=OrderStatus.ready)
    created_at = db.Column(db.DateTime, default=datetime.now())
    order_details = db.relationship("OrderDetail")


class OrderDetail(db.Model):
    __tablename__ = "orderDetail"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(Order.id))
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id))
    count = db.Column(db.Integer)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now())
