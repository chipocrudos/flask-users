import os

import pytest
from config import Configuration, db, logger
from config.app import create_app
from sqlalchemy import create_engine

USER = {
    "email": "test_user@email.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "M1npassw0rd",
    "confirm_password": "M1npassw0rd",
}


class ConfigTest(Configuration):

    MYSQL_DATABASE = "fusers_test"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")

    def __init__(self) -> None:
        super().__init__()

        BASE_URI = (
            "mysql+pymysql://"
            f"{self.MYSQL_USER}"
            f":{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}"
            f":{self.MYSQL_PORT}"
        )

        self.SQLALCHEMY_DATABASE_URI = f"{BASE_URI}" f"/{self.MYSQL_DATABASE}"
        self.SQLALCHEMY_DEFAULT_DATABASE_URI = f"{BASE_URI}" "/mysql"


@pytest.fixture(scope="session")
def test_config():

    _test_config = ConfigTest()
    engine_default = create_engine(_test_config.SQLALCHEMY_DEFAULT_DATABASE_URI)
    conn = engine_default.connect()
    conn.execute("COMMIT")
    conn.execute(f"DROP DATABASE IF EXISTS {_test_config.MYSQL_DATABASE};")
    conn.execute(f"CREATE DATABASE {_test_config.MYSQL_DATABASE};")
    conn.close()

    yield _test_config

    conn = engine_default.connect()
    conn.execute("COMMIT")
    conn.execute(f"DROP DATABASE IF EXISTS {_test_config.MYSQL_DATABASE};")
    conn.close()


@pytest.fixture(scope="session")
def app(test_config):

    _app = create_app(test_config)

    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="session")
def client(app):

    _client = app.test_client()

    db.create_all()

    yield _client

    # db.drop_all()
