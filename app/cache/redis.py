import redis.asyncio as redis
from redis.asyncio.client import Redis

from core.config import settings
from exceptions.redis import RedisClientNotInitializedException


class RedisHelper:
    def __init__(self) -> None:
        self._client: Redis | None = None

    async def connect(self) -> None:
        self._client = redis.from_url(str(settings.redis.url), decode_responses=True)
        await self._client.ping()  # type: ignore[misc]

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    def get_client(self) -> Redis:
        if self._client is None:
            raise RedisClientNotInitializedException()
        return self._client


redis_helper = RedisHelper()
