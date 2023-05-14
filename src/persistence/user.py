import bson
import hashlib

import pydantic
import pymongo.collection

from src.config import CONFIG
from src.log import get_logger


LOGGER = get_logger(__name__, CONFIG.app_name)


class UserExistsError(FileExistsError):
    ...


class User(pydantic.BaseModel):
    _id: bson.objectid.ObjectId | None
    username: str
    hashed_password: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            bson.objectid.ObjectId: str
        }


async def create_user(
        collection: pymongo.collection.Collection,
        username: str,
        password: str
) -> User:
    LOGGER.debug(f'Collection: {collection.name} :: Username: {username} :: Password: ****')
    user = await read_user(collection, username)
    if user is not None:
        LOGGER.critical(f'User: {username} already exists in the {collection.name} Collection')
        raise UserExistsError(f'User {username} exists.')
    LOGGER.debug(f'User ({username} does not yet exist, proceeding with creating a new user)')
    password = hashlib.sha256(password.encode()).hexdigest()
    user = User(
        _id=bson.objectid.ObjectId(),
        username=username,
        hashed_password=password
    )
    collection.insert_one(user.dict())
    LOGGER.debug(f'User ({username}) inserted into Collection ({collection.name})')
    return user


async def read_user(
        collection: pymongo.collection.Collection,
        username: str
) -> User | None:
    LOGGER.debug(f'Read User Attempt: {username}')
    user = collection.find_one({'username': username})
    if user:
        LOGGER.debug(f'User Found: {username}')
        return User(**user)
    LOGGER.debug(f'User ({username}) Not Found')
    return None


async def update_user(
        collection: pymongo.collection.Collection,
        username: str,
        password: str
) -> User:
    LOGGER.debug(f'Attempting to update a User ({username})')
    user = await read_user(collection, username)
    if user is None:
        LOGGER.critical(f'User {username} does not exist, unable to update')
        raise UserExistsError(f'User {username} does not exist.')
    password = hashlib.sha256(password.encode()).hexdigest()
    collection.update_one(
        filter={'username': user.username},
        update={'hashed_password': password}
    )
    LOGGER.debug(f"User {username}'s password has been successfully updated")
    return await read_user(collection, username)


async def delete_user(
        collection: pymongo.collection.Collection,
        username: str
) -> None:
    LOGGER.debug(f'Attempting user deletion for User ({username})')
    collection.delete_one(filter={'username': username})
    LOGGER.debug(f'User ({username}) deleted')


if __name__ == '__main__':  # pragma: no cover
    pass
