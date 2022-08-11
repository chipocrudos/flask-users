from http import HTTPStatus

from config import db
from flask import jsonify, make_response, request
from marshmallow.exceptions import ValidationError
from models.users import User as UserModel
from schemas.users import me_update_schema, user_schema, users_schema
from tools.jwt_token import get_jwt_payload


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
        is_active=True
    )
    db.session.add(db_user)
    db.session.commit()
    db.session.refresh(db_user)
    return make_response(user_schema.dump(db_user), HTTPStatus.CREATED)


def list_users_view():
    limit = request.args.get("limit", 10)
    offset = request.args.get("offset", 0)

    users = UserModel.query.offset(offset).limit(limit).all()

    return make_response(jsonify(users_schema.dump(users)), HTTPStatus.OK)


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


def me_view():
    payload = get_jwt_payload()
    db_user = UserModel.query.filter_by(email=payload["email"]).first()

    return make_response(user_schema.dump(db_user),
                         HTTPStatus.ACCEPTED)
