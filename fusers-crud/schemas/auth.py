from config.extensions import ma
from marshmallow import fields


class LoginSchema(ma.Schema):
    email = fields.String(required=True)
    password = fields.String(load_only=True)


login_schema = LoginSchema()


class TokenPayloadSchema(ma.Schema):
    id = fields.Integer(required=True)
    email = fields.String(required=True)
    is_active = fields.Boolean()


token_payload_schema = TokenPayloadSchema()
