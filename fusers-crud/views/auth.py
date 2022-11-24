from http import HTTPStatus

from config import DOCS_PATH, Configuration, db, urlsafe
from flasgger import swag_from
from flask import jsonify, make_response, request
from middleware.token import validate_url_token
from models.users import User as UserModel
from schemas.auth import (email_schema, login_schema, password_confirm_schema,
                          token_payload_schema, user_register_schema)
from tools.jwt_token import create_access_token
from tools.passwords import encrypt_password, validate_password
from tools.send_mail import send_email


@swag_from(f"{DOCS_PATH}/auth/login.yaml")
def login_view():

    args = request.get_json()
    user = login_schema.load(args)

    login_user = UserModel.query.filter_by(
                    email=user["email"],
                    is_active=True
                 ).first()

    if not login_user:
        return make_response(jsonify("User or password incorrect"),
                             HTTPStatus.BAD_REQUEST)

    if login_user.hashed_password is None or not validate_password(
                    user["password"],
                    login_user.hashed_password):
        return make_response(jsonify("User or password incorrect"),
                             HTTPStatus.BAD_REQUEST)

    access_token = create_access_token(token_payload_schema.dump(login_user))

    return make_response(jsonify({"token": access_token}), HTTPStatus.OK)


@swag_from(f"{DOCS_PATH}/auth/registration_user.yaml")
def registration_user_view():

    args = request.get_json()

    user = user_register_schema.load(args)

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
    token = urlsafe.dumps(email_schema.dump(db_user),
                          salt=Configuration.USERS_ACTIVATE_SALT)
    send_email("registration_user", "Registration completed",
                db_user, token=token,
                url_front=Configuration.URL_FRONT)

    return make_response(
            jsonify(
                    "User register complete,"
                    "check your mailbox to "
                    "proceed with activation account"
            ),
            HTTPStatus.CREATED
        )


@validate_url_token(Configuration.USERS_ACTIVATE_SALT,
                    Configuration.USERS_ACTIVATE_TOKEN_AGE_IN_SECONDS)
@swag_from(f"{DOCS_PATH}/auth/active_user.yaml")
def active_user_view(payload):

    exist_user = UserModel.query.filter_by(email=payload["email"]).first()

    if exist_user and not exist_user.is_active:
        exist_user.is_active = True
        db.session.commit()

    return make_response(
            jsonify("User active successfully"),
            HTTPStatus.OK
        )


@validate_url_token(Configuration.USERS_RESET_PASSWORD_SALT,
                    Configuration.USERS_RESET_PASSWORD_TOKEN_AGE_IN_SECONDS)
@swag_from(f"{DOCS_PATH}/auth/change_password.yaml")
def change_password_view(payload):
    args = request.get_json()

    passwords = password_confirm_schema.load(args)

    exist_user = UserModel.query.filter_by(email=payload["email"]).first()

    if exist_user and exist_user.is_active:
        exist_user.hashed_password = encrypt_password(passwords["password"])
        db.session.commit()

    return make_response(
            jsonify("Your password has by updated"),
            HTTPStatus.OK
        )


@swag_from(f"{DOCS_PATH}/auth/password_recovery.yaml")
def password_recovery_view():

    args = request.get_json()

    email = email_schema.load(args)

    exist_user = UserModel.query.filter_by(email=email["email"]).first()

    if exist_user and exist_user.is_active:
        token = urlsafe.dumps(email,
                             salt=Configuration.USERS_RESET_PASSWORD_SALT)
        send_email("recovery_password", "Password recovery",
                   exist_user, token=token,
                   url_front=Configuration.URL_FRONT)

    return make_response(
            jsonify("Email has by sended with instruction"),
            HTTPStatus.OK
        )
