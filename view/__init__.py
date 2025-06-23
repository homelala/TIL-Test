from view.test import TestView


def register_app(app):
    TestView.register(app,route_base="/test", trailing_slash=False)
