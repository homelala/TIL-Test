from marshmallow import Schema, fields


class OrderDetailSchema(Schema):
    product_id = fields.Integer(required=True)
    count = fields.Integer(required=True, default=1)
    price = fields.Integer(required=True)


class OrderSchema(Schema):
    user_id = fields.Integer(required=True)
    order_list = fields.Nested(OrderDetailSchema, many=True)
    address = fields.String(required=True)
