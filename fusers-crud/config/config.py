import os


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


def getenv_int(var_name, default_value=0):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = int(env_value)
    return result


class Configuration():
    DEBUG: bool = getenv_boolean("DEBUG")
    PASSWORD_KEY: str = os.getenv("PASSWORD_KEY", "set_complex_key")
    KEY_ENCODE: bytes = PASSWORD_KEY.encode("utf-8")

    TOKEN_KEY: str = os.getenv("TOKEN_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = getenv_int(
                "ACCESS_TOKEN_EXPIRE_MINUTES",
                30
            )

    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE")
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    MYSQL_PORT: int = getenv_int("MYSQL_PORT", 3306)
    MYSQL_HOST: str = os.getenv("MYSQL_HOST")

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://"
        f"{MYSQL_USER}"
        f":{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}"
        f":{MYSQL_PORT}"
        f"/{MYSQL_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
