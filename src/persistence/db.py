from typing import (
    Any,
    Callable,
    Coroutine,
    TypeVar,
)

import pymongo

from src.persistence.utils import get_mongo_client
from src.config import CONFIG
from src.log import get_logger


LOGGER = get_logger(__name__, CONFIG.app_name)
T = TypeVar('T')
DatabaseActionFuture = Coroutine[Any, Any, T | None]
DatabaseAction = Callable[
    [pymongo.collection.Collection, ...],
    DatabaseActionFuture
]


class Database:
    def __init__(
            self,
            username: str,
            password: str,
            project_name: str,
            database_name: str,
            collection_name: str,
            server_api: int = 1
    ):
        LOGGER.debug(
            f'Starting up a Database with the following settings:'
            f'\n\t-> Username: {username}'
            f'\n\t-> Password: ****'
            f'\n\t-> Project Name: {project_name}'
            f'\n\t-> Database Name: {database_name}'
            f'\n\t-> Collection Name: {collection_name}'
            f'\n\t-> Server API: {server_api}'
        )
        self._client = get_mongo_client(
            username=username,
            password=password,
            project_name=project_name,
            server_api=server_api
        )
        self._database = self._client.get_database(database_name)
        self._collection = self._database.get_collection(collection_name)

    @property
    def database(self) -> pymongo.database.Database:
        return self._database

    @property
    def collection(self) -> pymongo.collection.Collection:
        return self._collection


if __name__ == '__main__':  # pragma: no cover
    pass
