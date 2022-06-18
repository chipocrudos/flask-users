from http import HTTPStatus

from flask import jsonify, make_response, request
from marshmallow.exceptions import ValidationError
from models.users import User as UserModel
from schemas.auth import login_schema, token_payload_schema
from tools.jwt_token import create_access_token
from tools.passwords import validate_password


def login_view():

    args = request.get_json()

    try:
        user = login_schema.load(args)
    except ValidationError as err:
        return make_response(jsonify(err.messages), HTTPStatus.BAD_REQUEST)

    login_user = UserModel.query.filter_by(
                    email=user["email"],
                    is_active=True
                 ).first()

    if not login_user:
        return make_response(jsonify("User or password incorrect"),
                             HTTPStatus.BAD_REQUEST)

    if not validate_password(user["password"], login_user.hashed_password):
        return make_response(jsonify("User or password incorrect"),
                             HTTPStatus.BAD_REQUEST)

    access_token = create_access_token(token_payload_schema.dump(login_user))

    return make_response(jsonify({"token": access_token}), HTTPStatus.OK)
