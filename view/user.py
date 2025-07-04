from flask_classful import FlaskView, route
from flask_apispec import marshal_with, use_kwargs
from dto.user import UserSchema, RegisterUserSchema
from model.user import User
from database import db


class UserView(FlaskView):
    @route("/<int:user_id>")
    @marshal_with(UserSchema, code=200)
    def get(self, user_id):
        return User.query.filter_by(id=user_id).first(), 200

    @route("/", methods=["POST"])
    @use_kwargs(RegisterUserSchema, locations=["json"])
    @marshal_with(UserSchema, code=200)
    def post(self, name, email):
        user = User(name=name, email=email)

        db.session.add(user)
        db.session.commit()
        return user, 200

    @route("/<int:user_id>", methods=["PUT"])
    @use_kwargs(RegisterUserSchema, locations=["json"])
    @marshal_with(UserSchema, code=201)
    def put(self, user_id, name, email):
        user = User.query.filter_by(id=user_id).first()
        user.name = name
        user.email = email

        db.session.add(user)
        db.session.commit()

        return user, 201



