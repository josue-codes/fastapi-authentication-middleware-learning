from __future__ import annotations

import bson
import hashlib

import pydantic
import pymongo.collection
from pymongo import MongoClient
from pymongo.server_api import ServerApi


class UserExistsError(FileExistsError):
    ...


def get_mongo_client(
        username: str,
        password: str,
        project_name: str,
        server_api: int = 1
) -> MongoClient:
    uri = f'mongodb+srv://{username}:{password}@{project_name}.ptim0ok.mongodb.net/?retryWrites=true&w=majority'
    return MongoClient(uri, server_api=ServerApi(str(server_api)))


async def create_user(
        collection: pymongo.collection.Collection,
        username: str,
        password: str
) -> User:
    user = await read_user(collection, username)
    if user is not None:
        raise UserExistsError(f'User {username} exists.')
    password = hashlib.sha256(password.encode()).hexdigest()
    user = User(
        _id=bson.objectid.ObjectId(),
        username=username,
        hashed_password=password
    )
    collection.insert_one(user.dict())
    return user


async def delete_user(
        collection: pymongo.collection.Collection,
        username: str
) -> None:
    collection.delete_one(filter={'username': username})


async def read_user(
        collection: pymongo.collection.Collection,
        username: str
) -> User | None:
    user = collection.find_one({'username': username})
    if user:
        return User(**user)
    return None


async def update_user(
        collection: pymongo.collection.Collection,
        username: str,
        password: str
) -> User:
    user = await read_user(collection, username)
    if user is None:
        raise UserExistsError(f'User {username} does not exist.')
    password = hashlib.sha256(password.encode()).hexdigest()
    collection.update_one(
        filter={'username': user.username},
        update={'hashed_password': password}
    )
    return await read_user(collection, username)


class User(pydantic.BaseModel):
    _id: bson.objectid.ObjectId | None
    username: str
    hashed_password: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            bson.objectid.ObjectId: str
        }


class UserDatabase:

    def __init__(
            self,
            username: str,
            password: str,
            project_name: str,
            database_name: str,
            collection_name: str,
            server_api: int = 1
    ):
        self._client = get_mongo_client(
            username=username,
            password=password,
            project_name=project_name,
            server_api=server_api
        )
        self._user_database = self._client.get_database(database_name)
        self._user_collection = self._user_database.get_collection(collection_name)

    async def create_user(self, username: str, password: str) -> User:
        return await create_user(
            collection=self._user_collection,
            username=username,
            password=password
        )

    async def read_user(self, username: str) -> User | None:
        return await read_user(
            collection=self._user_collection,
            username=username
        )

    async def update_user(self, username: str, password: str) -> User | None:
        return await update_user(
            collection=self._user_collection,
            username=username,
            password=password
        )

    async def delete_user(self, username: str) -> None:
        return await delete_user(
            collection=self._user_collection,
            username=username
        )


if __name__ == '__main__':  # pragma: no cover
    pass
