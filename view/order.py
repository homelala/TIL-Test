from itertools import product

from flask_apispec import marshal_with, use_kwargs
from flask_classful import FlaskView, route

from dto.order import OrderSchema
from service.orderService import OrderService


class OrderView(FlaskView):
    @route("/", methods=["POST"])
    @use_kwargs(OrderSchema, code=200)
    def post(self, user_id, order_list, address):
        OrderService.order_product(user_id, address, order_list)
        return "", 200
