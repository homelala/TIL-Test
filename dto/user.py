from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    email = fields.String(required=True)


class RegisterUserSchema(Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
