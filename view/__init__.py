from view.order import OrderView
from view.test import TestView
from view.user import UserView


def register_app(app):
    TestView.register(app, route_base="/test", trailing_slash=False)
    UserView.register(app, route_base="/users", trailing_slash=False)
    OrderView.register(app, route_base="/orders", trailing_slash=False)