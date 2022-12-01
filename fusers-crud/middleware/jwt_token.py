from http import HTTPStatus

from config import Configuration
from flask import jsonify, make_response, request
from jose import JWTError, jwt


def validate_token():
    authorizaition = request.headers.get("authorization")

    if authorizaition is None:
        return make_response(jsonify("Token is not provided"), HTTPStatus.UNAUTHORIZED)

    try:
        token_type, token = authorizaition.split(" ")
        payload = jwt.decode(
            token, Configuration.TOKEN_KEY, algorithms=[Configuration.ALGORITHM]
        )

        if not (token_type == "Bearer" and payload.get("email")):
            return make_response(
                jsonify("Not valid token provided"), HTTPStatus.UNAUTHORIZED
            )

    except (JWTError, ValueError):
        return make_response(
            jsonify("Not valid token provided"), HTTPStatus.UNAUTHORIZED
        )
