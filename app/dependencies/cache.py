from typing import Annotated, TypeAlias

from fastapi import Depends
from redis.asyncio.client import Redis

from cache import redis_helper
from cache.invalidator import CacheInvalidatorBase
from schemas.cache import ModelCacheConfig

RedisDep: TypeAlias = Annotated[Redis, Depends(redis_helper.get_client)]


def get_countries_cache_invalidator(cache: RedisDep) -> CacheInvalidatorBase:
    return CacheInvalidatorBase(cache, ModelCacheConfig(), "countries")


def get_genres_cache_invalidator(cache: RedisDep) -> CacheInvalidatorBase:
    return CacheInvalidatorBase(cache, ModelCacheConfig(), "genres")


def get_persons_cache_invalidator(cache: RedisDep) -> CacheInvalidatorBase:
    return CacheInvalidatorBase(cache, ModelCacheConfig(), "persons")


def get_movie_person_cache_invalidator(cache: RedisDep) -> CacheInvalidatorBase:
    return CacheInvalidatorBase(cache, ModelCacheConfig(), "movie_person_associations")


def get_movie_cache_invalidator(cache: RedisDep) -> CacheInvalidatorBase:
    return CacheInvalidatorBase(cache, ModelCacheConfig(), "movies")


CountryCacheInvalidatorDep: TypeAlias = Annotated[CacheInvalidatorBase, Depends(get_countries_cache_invalidator)]
GenreCacheInvalidatorDep: TypeAlias = Annotated[CacheInvalidatorBase, Depends(get_genres_cache_invalidator)]
PersonCacheInvalidatorDep: TypeAlias = Annotated[CacheInvalidatorBase, Depends(get_persons_cache_invalidator)]
MoviePersonCacheInvalidatorDep: TypeAlias = Annotated[CacheInvalidatorBase, Depends(get_movie_person_cache_invalidator)]
MovieCacheInvalidatorDep: TypeAlias = Annotated[CacheInvalidatorBase, Depends(get_movie_cache_invalidator)]
