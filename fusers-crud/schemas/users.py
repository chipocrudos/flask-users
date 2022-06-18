from config.extensions import ma
from marshmallow import fields


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    email = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    date_create = fields.String(dump_only=True)
    password = fields.String(load_only=True)
    is_active = fields.Boolean()


user_schema = UserSchema()
users_schema = UserSchema(many=True)
