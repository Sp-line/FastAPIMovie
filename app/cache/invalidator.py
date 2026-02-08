from redis.asyncio.client import Redis as AsyncRedis

from schemas.cache import ModelCacheConfig


class CacheInvalidatorBase[
    TModelCacheConfig: ModelCacheConfig
]:
    def __init__(
            self,
            cache: AsyncRedis,
            model_cache_config: TModelCacheConfig,
            table_name: str,
    ) -> None:
        self._cache = cache
        self._model_cache = model_cache_config
        self._table_name = table_name

    async def _invalidate_list_cache_butch(self, match: str) -> None:
        keys = []
        async for key in self._cache.scan_iter(match=match):
            keys.append(key)
        if keys:
            await self._cache.delete(*keys)

    async def invalidate_list_cache(self) -> None:
        await self._invalidate_list_cache_butch(f"{self._table_name}:list*")

    async def invalidate_retrieve_cache(self, *ids: int) -> None:
        keys = [self._model_cache.retrieve_key.format(
            table_name=self._table_name,
            obj_id=obj_id,
        ) for obj_id in ids]
        await self._cache.delete(*keys)
