from config.extensions import ma
from marshmallow import fields


class UserMeUpdateSchema(ma.Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)


me_update_schema = UserMeUpdateSchema()


class UserSchema(UserMeUpdateSchema):
    id = fields.Integer(dump_only=True)
    email = fields.String(required=True)
    date_create = fields.String(dump_only=True)
    password = fields.String(load_only=True)
    is_active = fields.Boolean()


user_schema = UserSchema()
users_schema = UserSchema(many=True)
