from __future__ import annotations

import time
import pathlib
from typing import Dict

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    Response
)
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.auth import (
    authenticate_api_key,
    authenticate_auth_token,
    generate_auth_token,
)


STATIC_DIRECTORY = pathlib.Path(__file__).parent / 'static'


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


# APP.add_middleware(
#     CORSMiddleware,
#     allow_origins=['*'],
#     allow_credentials=True,
#     allow_methods=['*'],
#     allow_headers=['*'],
# )


@APP.post('/auth/token')
async def authenticate_user(api_key: bool = Depends(authenticate_api_key)):
    if api_key:
        auth_token = generate_auth_token()
        AUTH_TOKENS[auth_token] = time.time()
        return {'auth_token': auth_token}
    raise HTTPException(status_code=401, detail='Unauthorized')


@APP.middleware('https')
async def auth_middleware(request: Request, call_next):
    if request.url.path == '/auth/token':
        response = await call_next(request)
    else:
        if authenticate_auth_token(request, AUTH_TOKENS):
            response = await call_next(request)
        else:
            response = Response(status_code=401, content='Unauthorized')

    return response


@APP.get('/secure/data')
async def get_secure_data():
    return {"data": "This is secure data"}


if __name__ == '__main__':  # pragma: no cover
    uvicorn.run(
        app=APP,
        host='0.0.0.0',
        port=443
    )
