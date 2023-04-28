from __future__ import annotations

from uuid import uuid4
import hashlib
import time

from fastapi.security import APIKeyHeader

from src.config import Config

api_key_header = APIKeyHeader(name="api_key", auto_error=False)


def authenticate_api_key(api_key: str | None) -> bool:
    return api_key == Config().api_key


def generate_auth_token() -> str:
    token = str(uuid4())
    hashed_token = hashlib.sha256(token.encode()).hexdigest()
    return hashed_token


def authenticate_auth_token(request, auth_tokens):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return False
    auth_token = auth_header.split(" ")[-1]
    if auth_token not in auth_tokens:
        return False
    token_age = time.time() - auth_tokens[auth_token]
    return token_age < 28800  # 8 hours


if __name__ == '__main__':  # pragma: no cover
    pass
