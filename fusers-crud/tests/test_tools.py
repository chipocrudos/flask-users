from http import HTTPStatus

from flask import url_for


def test_prefech_method(client):
    response = client.options(
        url_for("app.users.me_view"),
        headers={"Content-type": "application/json"},
    )

    assert response.status_code == HTTPStatus.OK.value
