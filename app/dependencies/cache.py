from typing import Annotated, TypeAlias

from fastapi import Depends
from redis.asyncio.client import Redis

from cache import redis_helper

RedisDep: TypeAlias = Annotated[Redis, Depends(redis_helper.get_client)]
