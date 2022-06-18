from datetime import datetime, timedelta

from config.config import Configuration
from flask import request
from jose import jwt


def create_access_token(data):
    to_encode = data.copy()

    expire = datetime.utcnow() + \
        timedelta(minutes=Configuration.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Configuration.TOKEN_KEY,
                             algorithm=Configuration.ALGORITHM)
    return encoded_jwt


def get_jwt_payload():
    authorizaition = request.headers.get('authorization')

    token_type, token = authorizaition.split(" ")
    payload = jwt.decode(token,
                         Configuration.TOKEN_KEY,
                         algorithms=[Configuration.ALGORITHM])

    return payload
