from redis.asyncio.client import Redis as AsyncRedis

from cache.invalidator import CacheInvalidatorBase
from schemas.movie import MovieCacheConfig


class MovieCacheInvalidator(CacheInvalidatorBase[MovieCacheConfig]):
    def __init__(self, cache: AsyncRedis) -> None:
        super().__init__(
            cache,
            MovieCacheConfig(),
            "movies"
        )

    async def invalidate_list_summary_cache(self) -> None:
        await self._invalidate_list_cache_butch(f"{self._table_name}:list:summary*")

    async def invalidate_detail_cache(self, *ids: int) -> None:
        keys = [self._model_cache.detail_key.format(
            table_name=self._table_name,
            obj_id=obj_id,
        ) for obj_id in ids]
        await self._cache.delete(*keys)
