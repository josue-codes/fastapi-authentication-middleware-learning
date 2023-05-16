import sys
import pathlib
from typing import Dict

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    status,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from fastapi.responses import JSONResponse
import uvicorn

from src.auth import (
    generate_auth_token,
    token_expired,
    submitted_password_matches_database,
)
from src.persistence.db import Database
from src.persistence.user import (
    UserExistsError,
    User,
    create_user,
    read_user,
)
from src.persistence.auth_token import (
    create_token,
    read_token,
    delete_token,
)
from src.config import CONFIG
from src.log import get_logger


STATIC_DIRECTORY = pathlib.Path(__file__).parent / 'static'

LOGGER = get_logger(__name__, CONFIG.app_name)


def log_exception(exc_type, exc_value, exc_traceback):
    LOGGER.critical(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_traceback),
    )


sys.excepthook = log_exception

USER_DATABASE = Database(
    username=CONFIG.db_username,
    password=CONFIG.db_password,
    project_name=CONFIG.db_project_name,
    database_name=CONFIG.db_name_user,
    collection_name=CONFIG.db_collection_name_user
)
TOKEN_DATABASE = Database(
    username=CONFIG.db_username,
    password=CONFIG.db_password,
    project_name=CONFIG.db_project_name,
    database_name=CONFIG.db_name_token,
    collection_name=CONFIG.db_collection_name_token
)


APP = FastAPI()
AUTH_TOKENS: Dict[str, float] = {}


async def authenticate_user(username: str, password: str) -> User | None:
    LOGGER.debug(f'Attempting to authenticate User {username}')
    user: User | None = await read_user(USER_DATABASE.collection, username)
    if user and submitted_password_matches_database(password, user.hashed_password):
        LOGGER.debug(f'User {username} authenticated')
        return user
    LOGGER.debug(f'User {username} failed authentication')
    return None


@APP.post('/signup')
async def signup(request: Request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')
    try:
        user: User = await create_user(USER_DATABASE.collection, username, password)
    except UserExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    return JSONResponse({'username': user.username})


@APP.post('/login')
async def login(request: Request):
    data = await request.json()
    LOGGER.debug(
        f'Login data: Username - {data.get("username")} '
        f'-- Password - {"*" if data.get("password") else "blank / missing"}'
    )
    username = data.get('username')
    password = data.get('password')
    user = await authenticate_user(username, password)
    if user:
        access_token = generate_auth_token({'username': user.username})
        LOGGER.debug('Access Token created')
        await create_token(TOKEN_DATABASE.collection, access_token)
        LOGGER.debug('Access Token stored')
        return {'access_token': access_token, 'token_type': 'bearer'}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


# @APP.middleware('http')
# async def auth_middleware(request: Request, call_next):
#     if request.url.path in ['/', '/auth/token']:
#         response = await call_next(request)
#     else:
#         if authenticate_auth_token(request, AUTH_TOKENS):
#             response = await call_next(request)
#         else:
#             response = Response(status_code=401, content='Unauthorized')
#
#     return response


security = HTTPBearer()


async def verify_token(
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if not credentials or not credentials.scheme.lower() == 'bearer':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials'
        )
    token = credentials.credentials
    db_token = await read_token(TOKEN_DATABASE.collection, token)
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )
    if token_expired(token):
        await delete_token(TOKEN_DATABASE.collection, token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Expired token'
        )
    return token


@APP.get('/secure/data')
async def get_secure_data(_: str = Depends(verify_token)):
    return {'data': 'This is secure data'}


if __name__ == '__main__':  # pragma: no cover
    uvicorn.run(
        app=APP,
        host='0.0.0.0',
        port=8888
    )
