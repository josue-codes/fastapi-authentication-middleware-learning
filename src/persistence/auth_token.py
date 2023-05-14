import bson

import pydantic
import pymongo.collection

from src.log import get_logger
from src.config import CONFIG


LOGGER = get_logger(__name__, CONFIG.app_name)


class Token(pydantic.BaseModel):
    _id: bson.objectid.ObjectId | None
    token: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            bson.objectid.ObjectId: str
        }


async def create_token(
        collection: pymongo.collection.Collection,
        token: str
) -> Token:
    LOGGER.debug(f'Collection: {collection.name} :: Token: {token}')
    auth_token = Token(
        _id=bson.objectid.ObjectId(),
        token=token,
    )
    LOGGER.debug(f'Token pydantic class created: {auth_token} :: {auth_token.dict()}')
    collection.insert_one(auth_token.dict())
    LOGGER.debug(f'Token ({token}) inserted into Collection ({collection.name})')
    return auth_token


async def read_token(
        collection: pymongo.collection.Collection,
        token: str
) -> Token | None:
    LOGGER.debug(f'Read Token Attempt: {token}')
    auth_token = collection.find_one({'token': token})
    if auth_token:
        LOGGER.debug(f'Token Found: {token}')
        return Token(**auth_token)
    LOGGER.debug(f'Token Not Found')
    return None


async def delete_token(
        collection: pymongo.collection.Collection,
        token: str
) -> None:
    LOGGER.debug(f'Attempting token deletion for Token ({token})')
    collection.delete_one(filter={'token': token})
    LOGGER.debug(f'Token ({token}) deleted')


if __name__ == '__main__':  # pragma: no cover
    pass
