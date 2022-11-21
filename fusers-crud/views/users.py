from http import HTTPStatus

from config import DOCS_PATH, db
from flasgger import swag_from
from flask import jsonify, make_response, request
from flask_cors import cross_origin
from marshmallow.exceptions import ValidationError
from models.users import User as UserModel
from schemas.users import me_update_schema, user_schema, users_schema
from tools.jwt_token import get_jwt_payload


@swag_from(f"{DOCS_PATH}/users/create_user.yaml")
def create_user_view():

    args = request.get_json()

    try:
        user = user_schema.load(args)
    except ValidationError as err:
        return make_response(jsonify(err.messages), HTTPStatus.BAD_REQUEST)

    exist_user = UserModel.query.filter_by(email=user["email"]).first()

    if exist_user:
        return make_response(jsonify("User exist"), HTTPStatus.BAD_REQUEST)

    db_user = UserModel(
        email=user["email"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        is_active=user["is_active"],
        is_super=user["is_super"]
    )
    db.session.add(db_user)
    db.session.commit()
    db.session.refresh(db_user)
    return make_response(user_schema.dump(db_user), HTTPStatus.CREATED)


@swag_from(f"{DOCS_PATH}/users/list_users.yaml")
def list_users_view():

    limit = request.args.get("limit", 10)
    offset = request.args.get("offset", 0)

    users = UserModel.query.offset(offset).limit(limit).all()

    return make_response(jsonify(users_schema.dump(users)), HTTPStatus.OK)


@swag_from(f"{DOCS_PATH}/users/get_user.yaml")
def get_user_view(id):
    user = UserModel.query.filter_by(id=id).first()
    if not user:
        return make_response("User not exist", HTTPStatus.NOT_FOUND)

    return make_response(jsonify(user_schema.dump(user)), HTTPStatus.OK)


@swag_from(f"{DOCS_PATH}/users/me_update.yaml")
def me_update_user_view():

    args = request.get_json()
    payload = get_jwt_payload()

    try:
        user = me_update_schema.load(args)
    except ValidationError as err:
        return make_response(jsonify(err.messages), HTTPStatus.BAD_REQUEST)

    db_user = UserModel.query.filter_by(email=payload["email"]).first()

    if db_user is None:
        return make_response("User not exist", HTTPStatus.NOT_FOUND)

    db_user.first_name = user.get("first_name")
    db_user.last_name = user.get("last_name")

    db.session.commit()
    db.session.refresh(db_user)

    return make_response(user_schema.dump(db_user), HTTPStatus.OK)


@swag_from(f"{DOCS_PATH}/users/me.yaml")
def me_view():
    payload = get_jwt_payload()
    db_user = UserModel.query.filter_by(email=payload["email"]).first()
    return make_response(user_schema.dump(db_user),
                         HTTPStatus.OK)
