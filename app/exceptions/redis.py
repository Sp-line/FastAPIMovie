class RedisException(Exception):
    pass


class RedisClient(RedisException):
    pass


class RedisClientNotInitializedException(RedisClient):
    def __init__(self) -> None:
        super().__init__("Redis Client is not initialized. Call connect() inside lifespan or startup event.")
