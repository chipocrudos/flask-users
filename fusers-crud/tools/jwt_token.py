from datetime import datetime, timedelta
from uuid import uuid4

from config import Configuration
from flask import request
from jose import jwt


def create_access_token(data):
    to_encode = data.copy()

    issue_at = datetime.utcnow()
    expire = issue_at + \
        timedelta(minutes=Configuration.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"iat": issue_at})
    to_encode.update({"exp": expire})
    to_encode.update({"jti": str(uuid4())})
    encoded_jwt = jwt.encode(to_encode, Configuration.TOKEN_KEY,
                             algorithm=Configuration.ALGORITHM)
    return encoded_jwt


def get_jwt_payload():
    authorizaition = request.headers.get('authorization')

    _, token = authorizaition.split(" ")
    payload = jwt.decode(token,
                         Configuration.TOKEN_KEY,
                         algorithms=[Configuration.ALGORITHM])

    return payload
