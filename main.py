from __future__ import annotations

import hashlib
import pathlib
from typing import Dict

from fastapi import (
    FastAPI,
    HTTPException,
    status
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn

from src.auth import generate_auth_token
from src.db import UserDatabase, UserExistsError
from src.config import Config


STATIC_DIRECTORY = pathlib.Path(__file__).parent / 'static'
CONFIG = Config()
USER_DATABASE = UserDatabase(
    username=CONFIG.db_username,
    password=CONFIG.db_password,
    project_name=CONFIG.db_project_name,
    database_name=CONFIG.db_name,
    collection_name=CONFIG.db_collection_name
)


APP = FastAPI()
AUTH_TOKENS: Dict[str, float] = {}


for file_sys_obj in STATIC_DIRECTORY.iterdir():
    if file_sys_obj.is_file():
        continue
    APP.mount(
        path=f'/{file_sys_obj.name}',
        app=StaticFiles(directory=file_sys_obj.absolute()),
        name=file_sys_obj.name
    )


@APP.get("/")
async def root():
    return {"message": "Please authenticate at /login to access other routes."}


async def authenticate_user(username: str, password: str):
    user = await USER_DATABASE.read_user(username)
    if user and user.hashed_password == hashlib.sha256(password.encode()).hexdigest():
        return user
    return None


@APP.post('/create-user')
async def create_user(username: str, password: str):
    try:
        user = await USER_DATABASE.create_user(username, password)
    except UserExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    return JSONResponse({'username': user.username})


@APP.post('/login')
async def login(username: str, password: str):
    user = await authenticate_user(username, password)
    if user:
        access_token = generate_auth_token({'username': user.username})
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


@APP.get('/secure/data')
async def get_secure_data():
    return {"data": "This is secure data"}


if __name__ == '__main__':  # pragma: no cover
    uvicorn.run(
        app=APP,
        host='0.0.0.0',
        port=80
    )
