from flask_classful import FlaskView, route

from model.user import User


class UserView(FlaskView):
    @route("/")
    def get(self, name):
        return User.query.filter_by(name=name).first()

