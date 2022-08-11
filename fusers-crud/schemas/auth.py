import re
from enum import Enum

from config.extensions import ma
from marshmallow import (ValidationError, fields, validate, validates,
                         validates_schema)

from .users import UserSchema


class PasswordStrong(Enum):
    LESS = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
    LESS_ERROR = "Minimum eight characters, at least one letter and one number"
    NORMAL = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
    NORMAL_ERROR = (
        "Minimum eight characters, at least one uppercase letter, "
        "one lowercase letter and one number"
    )
    MOST = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    MOST_ERROR = (
        "Minimum eight characters, at least one letter, "
        "one number and one special character"
    )

    STRONGER = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    STRONGER_ERROR = (
        "Minimum eight characters, at least one uppercase letter, "
        "one lowercase letter, one number and one special character"
    )


class MailSchema(ma.Schema):
    email = fields.Email(require=True)


email_schema = MailSchema()


class PasswordSchema(ma.Schema):
    password = fields.String(
        required=True,
        validate=validate.Length(min=8))

    @validates("password")
    def validate_password(self, password):
        match = re.match(PasswordStrong.LESS.value, password)
        if not match:
            raise ValidationError(
                PasswordStrong.LESS_ERROR.value
            )


class LoginSchema(MailSchema):
    password = fields.String(load_only=True)


login_schema = LoginSchema()


class TokenPayloadSchema(ma.Schema):
    id = fields.Integer(required=True)
    email = fields.String(required=True)
    is_active = fields.Boolean()


token_payload_schema = TokenPayloadSchema()


class PasswordConfimSchema(PasswordSchema):

    confirm_password = fields.String()

    @validates_schema
    def validate_confirm_password(self, data, **kwargs):
        errors = {"confirm_password": "Password don't match"}
        if not data.get("password", "") == data.get("confirm_password"):
            raise ValidationError(errors)


password_confirm_schema = PasswordConfimSchema()


class UserRegisterSchema(UserSchema, PasswordConfimSchema):
    pass

user_register_schema = UserRegisterSchema()
