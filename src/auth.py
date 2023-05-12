from __future__ import annotations

import os
import datetime

import jwt


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
AUTH_TOKEN_EXPIRE_MINUTES = 600


def generate_auth_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=AUTH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


if __name__ == '__main__':  # pragma: no cover
    pass
