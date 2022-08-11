from http import HTTPStatus

from config import Configuration, db, urlsafe
from flask import jsonify, make_response, request
from marshmallow.exceptions import ValidationError
from middleware.token import validate_url_token
from models.users import User as UserModel
from schemas.auth import (email_schema, login_schema, password_confirm_schema,
                          token_payload_schema, user_register_schema)
from tools.jwt_token import create_access_token
from tools.passwords import encrypt_password, validate_password
from tools.send_mail import send_email


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

    if login_user.hashed_password is None or not validate_password(user["password"], login_user.hashed_password):
        return make_response(jsonify("User or password incorrect"),
                             HTTPStatus.BAD_REQUEST)

    access_token = create_access_token(token_payload_schema.dump(login_user))

    return make_response(jsonify({"token": access_token}), HTTPStatus.OK)


# Register user

def registration_user_view():

    args = request.get_json()

    try:
        user = user_register_schema.load(args)
    except ValidationError as err:
        return make_response(jsonify(err.messages), HTTPStatus.BAD_REQUEST)

    exist_user = UserModel.query.filter_by(email=user["email"]).first()

    if exist_user:
        return make_response(jsonify("User exist"), HTTPStatus.BAD_REQUEST)

    user["hashed_password"] = encrypt_password(user["password"])
    db_user = UserModel(
        email=user["email"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        hashed_password=user["hashed_password"],
    )
    db.session.add(db_user)
    db.session.commit()
    db.session.refresh(db_user)
    token = urlsafe.dumps(email_schema.dump(exist_user),
                          salt=Configuration.USERS_ACTIVATE_SALT)
    send_email("registration_user", "Registration completed",
                db_user, token=token,
                url_front=Configuration.URL_FRONT)

    return make_response("User register complete", HTTPStatus.CREATED)


@validate_url_token(Configuration.USERS_ACTIVATE_SALT,
                    Configuration.USERS_ACTIVATE_TOKEN_AGE_IN_SECONDS)
def active_user_view(payload):

    exist_user = UserModel.query.filter_by(email=payload["email"]).first()

    if exist_user and not exist_user.is_active:
        exist_user.is_active = True
        db.session.commit()

    return make_response("User active successfully", HTTPStatus.OK)


@validate_url_token(Configuration.USERS_RESET_PASSWORD_SALT,
                    Configuration.USERS_RESET_PASSWORD_TOKEN_AGE_IN_SECONDS)
def change_password_view(payload):
    args = request.get_json()

    try:
        passwords = password_confirm_schema.load(args)
    except ValidationError as err:
        return make_response(jsonify(err.messages), HTTPStatus.BAD_REQUEST)

    exist_user = UserModel.query.filter_by(email=payload["email"]).first()

    if exist_user and exist_user.is_active:
        exist_user.hashed_password = encrypt_password(passwords["password"])
        db.session.commit()

    return make_response("Your password has by updated", HTTPStatus.OK)


def password_recovery_view():

    args = request.get_json()

    try:
        email = email_schema.load(args)
    except ValidationError as err:
        return make_response(jsonify(err.messages), HTTPStatus.BAD_REQUEST)

    exist_user = UserModel.query.filter_by(email=email["email"]).first()

    if exist_user and exist_user.is_active:
        token = urlsafe.dumps(email,
                             salt=Configuration.USERS_RESET_PASSWORD_SALT)
        send_email("recovery_password", "Password recovery",
                   exist_user, token=token,
                   url_front=Configuration.URL_FRONT)

    return make_response("Email has by sended with instruction", HTTPStatus.OK)
