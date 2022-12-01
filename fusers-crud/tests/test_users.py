from email import header
from http import HTTPStatus
from http.client import NOT_FOUND

import pytest
from flask import url_for
from tools.jwt_token import create_access_token

from .conftest import USER

USER_LOGIN = {"id": 1, "is_active": True, "email": USER["email"]}

JWT_TOKEN = create_access_token(USER_LOGIN)
BEARER_TOKEN = f"Bearer {JWT_TOKEN}"

JWT_TOKEN_NOUSER = create_access_token(
    {"id": 2, "is_active": True, "email": "user@no.exist"}
)
BEARER_TOKEN_NOUSER = f"Bearer {JWT_TOKEN_NOUSER}"
JWT_TOKEN_NOUSER = create_access_token({"id": 2, "is_active": True})
BEARER_TOKEN_NOEMAIL = f"Bearer {JWT_TOKEN_NOUSER}"


@pytest.mark.parametrize(
    "token,test_input,expected",
    [
        (
            BEARER_TOKEN,
            {},
            HTTPStatus.OK.value,
        ),
        (
            BEARER_TOKEN,
            {"limit": 20},
            HTTPStatus.OK.value,
        ),
        (
            BEARER_TOKEN,
            {"limit": 20, "offset": 1},
            HTTPStatus.OK.value,
        ),
        (
            JWT_TOKEN,
            {},
            HTTPStatus.UNAUTHORIZED.value,
        ),
    ],
)
def test_list_users(token, test_input, expected, client):

    response = client.get(
        url_for("app.users.list_users_view"),
        query_string=test_input,
        headers={"Authorization": token},
    )

    assert response.status_code == expected


@pytest.mark.parametrize(
    "token,user_id,expected",
    [
        (
            BEARER_TOKEN,
            1,
            HTTPStatus.OK.value,
        ),
        (
            BEARER_TOKEN,
            10,
            HTTPStatus.NOT_FOUND.value,
        ),
        (
            BEARER_TOKEN + "a",
            1,
            HTTPStatus.UNAUTHORIZED.value,
        ),
        (
            JWT_TOKEN,
            1,
            HTTPStatus.UNAUTHORIZED.value,
        ),
    ],
)
def test_get_user(token, user_id, expected, client):

    response = client.get(
        url_for("app.users.get_user_view", id=user_id), headers={"Authorization": token}
    )

    assert response.status_code == expected


@pytest.mark.parametrize(
    "token,test_input,expected",
    [
        (
            BEARER_TOKEN,
            {x: USER[x] for x in ["first_name", "last_name"]},
            HTTPStatus.OK.value,
        ),
        (
            BEARER_TOKEN,
            {"first_name": USER["first_name"]},
            HTTPStatus.BAD_REQUEST.value,
        ),
        (
            BEARER_TOKEN,
            {"last_name": USER["last_name"]},
            HTTPStatus.BAD_REQUEST.value,
        ),
        (
            BEARER_TOKEN,
            {"first_name": "", "other_field": "not exist field"},
            HTTPStatus.BAD_REQUEST.value,
        ),
        (
            BEARER_TOKEN_NOUSER,
            {x: USER[x] for x in ["first_name", "last_name"]},
            HTTPStatus.NOT_FOUND.value,
        ),
    ],
)
def test_me_update_user(token, test_input, expected, client):

    response = client.put(
        url_for("app.users.me_update_user_view", id=1),
        json=test_input,
        headers={"Authorization": token},
    )

    assert response.status_code == expected


@pytest.mark.parametrize(
    "token,expected",
    [
        (
            BEARER_TOKEN,
            HTTPStatus.OK.value,
        ),
        (
            BEARER_TOKEN + "a",
            HTTPStatus.UNAUTHORIZED.value,
        ),
        (
            JWT_TOKEN,
            HTTPStatus.UNAUTHORIZED.value,
        ),
        (
            BEARER_TOKEN_NOEMAIL,
            HTTPStatus.UNAUTHORIZED.value,
        ),
        (
            "",
            HTTPStatus.UNAUTHORIZED.value,
        ),
    ],
)
def test_me(token, expected, client):

    response = client.get(
        url_for("app.users.me_view"), headers={"Authorization": token} if token else {}
    )

    assert response.status_code == expected


@pytest.mark.parametrize(
    "token,test_input,expected",
    [
        (
            BEARER_TOKEN,
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
            BEARER_TOKEN,
            {
                "email": "bad.email",
                "first_name": "firt name",
                "last_name": "last name",
                "is_active": True,
            },
            HTTPStatus.BAD_REQUEST.value,
        ),
        (
            BEARER_TOKEN + "a",
            {
                "email": "bad@email.com",
                "first_name": "firt name",
                "last_name": "last name",
                "is_active": True,
            },
            HTTPStatus.UNAUTHORIZED.value,
        ),
        (
            BEARER_TOKEN,
            {
                "email": "bad@email.com",
                "first_name": "firt name",
                "last_name": "last name",
                "is_active": True,
            },
            HTTPStatus.CREATED.value,
        ),
        (
            BEARER_TOKEN,
            {
                "email": "bad@email.com",
                "first_name": "firt name",
                "last_name": "last name",
                "is_active": True,
            },
            HTTPStatus.BAD_REQUEST.value,
        ),
    ],
)
def test_create_user(token, test_input, expected, client):

    response = client.post(
        url_for("app.users.create_user_view"),
        json=test_input,
        headers={"Authorization": token},
    )

    assert response.status_code == expected
