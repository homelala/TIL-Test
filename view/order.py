from flask_apispec import use_kwargs
from flask_classful import FlaskView, route

from dto.order import OrderSchema
from service.orderService import OrderService


class OrderView(FlaskView):
    @route("/", methods=["POST"])
    @use_kwargs(OrderSchema, code=200)
    def post(self, user_id, order_list, address):
        OrderService.order_product_correct_lock(user_id, address, order_list)
        return "", 200
