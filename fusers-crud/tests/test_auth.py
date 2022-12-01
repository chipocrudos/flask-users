from http import HTTPStatus
from time import sleep

import pytest
from config import urlsafe
from flask import url_for

from .conftest import USER, ConfigTest

ACTIVATE_TOKEN = urlsafe.dumps(USER, salt=ConfigTest.USERS_ACTIVATE_SALT)

RESET_TOKEN = urlsafe.dumps(
    {x: USER[x] for x in ["email"]}, salt=ConfigTest.USERS_RESET_PASSWORD_SALT
)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {
                "email": "",
                "first_name": "",
                "last_name": "",
                "password": "",
                "confirm_password": "",
            },
            HTTPStatus.BAD_REQUEST.value,
        ),
        (
            {
                "email": "bad.email",
                "first_name": "firt name",
                "last_name": "last name",
                "password": "sda",
                "confirm_password": "sda",
            },
            HTTPStatus.BAD_REQUEST.value,
        ),
        (
            {
                "email": "bad@email.com",
                "first_name": "firt name",
                "last_name": "last name",
                "password": "sda",
                "confirm_password": "sda",
            },
            HTTPStatus.BAD_REQUEST.value,
        ),
        (
            {
                "email": "bad@email.com",
                "first_name": "firt name",
                "last_name": "last name",
                "password": USER.get("password"),
                "confirm_password": USER.get("confirm_password") + "a",
            },
            HTTPStatus.BAD_REQUEST.value,
        ),
        (
            USER,
            HTTPStatus.CREATED.value,
        ),
        (
            USER,
            HTTPStatus.BAD_REQUEST.value,
        ),
    ],
)
def test_auth_registration_user(test_input, expected, client):

    response = client.post(url_for("app.auth.registration_user_view"), json=test_input)

    assert response.status_code == expected


@pytest.mark.parametrize(
    "token,delay,expected",
    [
        (ACTIVATE_TOKEN, 4, HTTPStatus.OK.value),
        (ACTIVATE_TOKEN, 0, HTTPStatus.BAD_REQUEST.value),
        (ACTIVATE_TOKEN + "a", 0, HTTPStatus.BAD_REQUEST.value),
    ],
)
def test_auth_active_user(token, delay, expected, client):

    response = client.get(url_for("app.auth.active_user_view", token=token))
    sleep(delay)

    assert response.status_code == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ({"email": "", "password": ""}, HTTPStatus.BAD_REQUEST.value),
        ({"email": "bad.email", "password": ""}, HTTPStatus.BAD_REQUEST.value),
        (
            {"email": "user@no-exist.com", "password": "no-exist"},
            HTTPStatus.BAD_REQUEST.value,
        ),
        (
            {"email": USER["email"], "password": "badpassword"},
            HTTPStatus.BAD_REQUEST.value,
        ),
        (
            {x: USER[x] for x in ["email", "password"]},
            HTTPStatus.OK.value,
        ),
    ],
)
def test_auth_login(test_input, expected, client):

    response = client.post(url_for("app.auth.login_view"), json=test_input)

    assert response.status_code == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ({"email": ""}, HTTPStatus.BAD_REQUEST.value),
        ({"email": "bad.email"}, HTTPStatus.BAD_REQUEST.value),
        (
            {"email": "user@no-exist.com"},
            HTTPStatus.OK.value,
        ),
        (
            {x: USER[x] for x in ["email"]},
            HTTPStatus.OK.value,
        ),
    ],
)
def test_auth_password_recovery(test_input, expected, client):

    response = client.post(url_for("app.auth.password_recovery_view"), json=test_input)

    assert response.status_code == expected


@pytest.mark.parametrize(
    "token,test_input,delay,expected",
    [
        (
            RESET_TOKEN,
            {x: USER[x] for x in ["password", "confirm_password"]},
            5,
            HTTPStatus.OK.value,
        ),
        (
            RESET_TOKEN,
            {
                "password": "sda",
                "confirm_password": "sda",
            },
            0,
            HTTPStatus.BAD_REQUEST.value,
        ),
        (
            RESET_TOKEN + "a",
            {
                "password": "sda",
                "confirm_password": "sda",
            },
            0,
            HTTPStatus.BAD_REQUEST.value,
        ),
        (
            RESET_TOKEN,
            {x: USER[x] for x in ["password", "confirm_password"]},
            0,
            HTTPStatus.BAD_REQUEST.value,
        ),
    ],
)
def test_auth_change_password(token, test_input, delay, expected, client):

    response = client.post(
        url_for("app.auth.change_password_view", token=token), json=test_input
    )
    sleep(delay)

    assert response.status_code == expected
