from typing import Annotated, TypeAlias

from fastapi import Depends
from redis.asyncio.client import Redis

from cache import redis_helper
from cache.invalidator import CacheInvalidatorBase
from schemas.cache import ModelCacheConfig

RedisDep: TypeAlias = Annotated[Redis, Depends(redis_helper.get_client)]


def get_countries_cache_invalidator(cache: RedisDep) -> CacheInvalidatorBase:
    return CacheInvalidatorBase(cache, ModelCacheConfig(), "countries")


CountryCacheInvalidatorDep: TypeAlias = Annotated[CacheInvalidatorBase, Depends(get_countries_cache_invalidator)]
