import os


class Config:
    @property
    def api_key(self) -> str:
        key = 'API_KEY'
        if os.getenv(key):
            return os.getenv(key)
        raise EnvironmentError(f'{key} environment variable not set.')

    @property
    def ssl_certfile(self) -> str:
        key = 'SSL_CERTFILE'
        if os.getenv(key):
            return os.getenv(key)
        raise EnvironmentError(f'{key} environment variable not set.')

    @property
    def ssl_keyfile(self) -> str:
        key = 'SSL_KEYFILE'
        if os.getenv(key):
            return os.getenv(key)
        raise EnvironmentError(f'{key} environment variable not set.')


if __name__ == '__main__':  # pragma: no cover
    pass
