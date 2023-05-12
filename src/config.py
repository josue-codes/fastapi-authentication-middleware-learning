import os


class Config:
    @property
    def secret_key(self) -> str:
        return get_env('SECRET_KEY')

    @property
    def db_username(self) -> str:
        return get_env('DB_USERNAME')

    @property
    def db_password(self) -> str:
        return get_env('DB_PASSWORD')

    @property
    def db_project_name(self) -> str:
        return get_env('DB_PROJECT_NAME')

    @property
    def db_name(self) -> str:
        return get_env('DB_NAME')

    @property
    def db_collection_name(self) -> str:
        return get_env('DB_COLLECTION_NAME')


def get_env(env_name: str) -> str:
    if os.getenv(env_name):
        return os.getenv(env_name)
    raise EnvironmentError(f'{env_name} environment variable not set.')


if __name__ == '__main__':  # pragma: no cover
    pass
