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

    async def invalidate_list_cache(self) -> None:
        keys = []
        async for key in self._cache.scan_iter(match=f"{self._table_name}:list*"):
            keys.append(key)
        if keys:
            await self._cache.delete(*keys)

    async def invalidate_retrieve_cache(self, obj_id: int) -> None:
        key = self._model_cache.retrieve_key.format(
            table_name=self._table_name,
            obj_id=obj_id,
        )
        await self._cache.delete(key)


