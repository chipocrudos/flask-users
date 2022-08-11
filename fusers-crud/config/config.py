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


def getenv_emails(var_name):
    env_value = os.getenv(var_name, "").split(",")
    return env_value


class Configuration():
    DEBUG: bool = getenv_boolean("DEBUG")
    URL_FRONT = os.getenv("URL_FRONT")

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

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = getenv_int("MAIL_PORT", 25)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    DONT_REPLY_FROM_EMAIL = getenv_emails("DONT_REPLY_FROM_EMAIL")
    ADMINS = getenv_emails("ADMINS")
    MAIL_USE_TLS = getenv_boolean("MAIL_USE_TLS", False)
    MAIL_USE_SSL = getenv_boolean("MAIL_USE_SSL", False)

    KEY_URL_TOKEN=os.getenv("KEY_URL_TOKEN")
    USERS_ACTIVATE_TOKEN_AGE_IN_SECONDS=getenv_int("USERS_ACTIVATE_TOKEN_AGE_IN_SECONDS")
    USERS_RESET_PASSWORD_TOKEN_AGE_IN_SECONDS=getenv_int(
            "USERS_RESET_PASSWORD_TOKEN_AGE_IN_SECONDS"
            )
    USERS_ACTIVATE_SALT = "ACTIVATE_USER"
    USERS_RESET_PASSWORD_SALT = "RESET_PASS"
