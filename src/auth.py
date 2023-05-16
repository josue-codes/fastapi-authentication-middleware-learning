import datetime
import hashlib

import jwt

from src.log import get_logger
from src.config import CONFIG


LOGGER = get_logger(__name__, CONFIG.app_name)
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def submitted_password_matches_database(
        submitted_password: str,
        database_password
) -> bool:
    LOGGER.debug('Attempting to hash and compare passwords')
    hashed_password = hashlib.sha256(submitted_password.encode()).hexdigest()
    matched = hashed_password == database_password
    LOGGER.debug(f'Password comparison evaluated to {matched}')
    return matched


def generate_auth_token(data: dict) -> str:
    LOGGER.debug(f'Attempting authorization Token generation for: {data}')
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=CONFIG.auth_token_expire_minutes)
    LOGGER.debug(f'Expiration for {data} set to {expire.strftime(DATE_FORMAT)}')
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, CONFIG.secret_key, algorithm=CONFIG.private_key_algorithm)
    LOGGER.debug('Authorization Token generated')
    return encoded_jwt


def decode_auth_token(token: str) -> dict | None:
    try:
        LOGGER.debug(f'Attempting to decode Token: {token}')
        return jwt.decode(token, CONFIG.secret_key, algorithms=[CONFIG.private_key_algorithm])
    except jwt.InvalidTokenError:
        LOGGER.critical(f'Token decoding failed for: {token}')
        return None


def token_expired(token: str) -> bool:
    LOGGER.debug(f'Checking is Token ({token}) is expired.')
    token = decode_auth_token(token)
    if not token:
        LOGGER.debug(f'Token ({token}) unable to be decoded so defaulting to "expired"')
        return True
    exp = token.get('exp')
    expiration = datetime.datetime.fromtimestamp(exp)
    current_time = datetime.datetime.now()
    LOGGER.debug(
        f'Token ({token}) expires at {expiration.strftime(DATE_FORMAT)} '
        f'and current time is {current_time.strftime(DATE_FORMAT)} '
        f':: {expiration < current_time}'
    )
    return expiration < current_time


if __name__ == '__main__':  # pragma: no cover
    pass
