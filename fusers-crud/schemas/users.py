from email.policy import default

from config.extensions import ma
from marshmallow import fields
from pkg_resources import require


class UserMeUpdateSchema(ma.Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)


me_update_schema = UserMeUpdateSchema()


class UserSchema(UserMeUpdateSchema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    date_create = fields.String(dump_only=True)
    password = fields.String(load_only=True)
    is_active = fields.Boolean()
    is_super = fields.Boolean(missing=False)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
