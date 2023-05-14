from pymongo import MongoClient
from pymongo.server_api import ServerApi


def get_mongo_client(
        username: str,
        password: str,
        project_name: str,
        server_api: int = 1
) -> MongoClient:
    uri = f'mongodb+srv://{username}:{password}@{project_name}.ptim0ok.mongodb.net/?retryWrites=true&w=majority'
    return MongoClient(uri, server_api=ServerApi(str(server_api)))


if __name__ == '__main__':  # pragma: no cover
    pass
