import bcrypt
from config.config import Configuration


def encrypt_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"),
                         Configuration.KEY_ENCODE)


def validate_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode("utf-8"),
                          hashed_password.encode("utf-8"))
