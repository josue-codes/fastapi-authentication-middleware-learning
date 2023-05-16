import os


class Config:
    @property
    def app_name(self):
        return 'auth'

    @property
    def secret_key(self) -> str:
        return get_env('SECRET_KEY')

    @property
    def auth_token_expire_minutes(self):
        return get_env('TOKEN_SESSION_DURATION')

    @property
    def private_key_algorithm(self):
        return get_env('ALGORITHM')

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
    def db_name_user(self) -> str:
        return get_env('DB_NAME_USER')

    @property
    def db_collection_name_user(self) -> str:
        return get_env('DB_COLLECTION_NAME_USER')

    @property
    def db_name_token(self) -> str:
        return get_env('DB_NAME_TOKEN')

    @property
    def db_collection_name_token(self) -> str:
        return get_env('DB_COLLECTION_NAME_TOKEN')


def get_env(env_name: str) -> str:
    if os.getenv(env_name):
        return os.getenv(env_name)
    raise EnvironmentError(f'{env_name} environment variable not set.')


CONFIG = Config()


if __name__ == '__main__':  # pragma: no cover
    pass
