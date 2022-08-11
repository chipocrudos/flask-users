from functools import wraps
from http import HTTPStatus

from config import urlsafe
from flask import make_response
from itsdangerous.exc import BadSignature, SignatureExpired


def validate_url_token(salt, age):
    def decorator(f):
        @wraps(f)
        def decorate_fun(**kwargs):
            data = None

            try:
                data = urlsafe.loads(
                    kwargs.get("token"),
                    salt=salt,
                    max_age=age
                )
            except SignatureExpired:
                return make_response("Signature expired", HTTPStatus.BAD_REQUEST)

            except (BadSignature, TypeError, ValueError):
                return make_response("Bad signature", HTTPStatus.BAD_REQUEST)

            return f(data)

        return decorate_fun
    return decorator
