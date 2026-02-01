from abc import ABC
from typing import Any

import orjson
from pydantic import BaseModel
from redis.asyncio.client import Redis as AsyncRedis

from repositories.base import RepositoryBase
from repositories.unit_of_work import UnitOfWork
from schemas.cache import ModelCacheConfig
from services.abc import ServiceABC


class CacheServiceABC[
    RepositoryBaseType: RepositoryBase,
    ReadSchemaType: BaseModel,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
    DBCreateSchemaType: BaseModel,
    DBUpdateSchemaType: BaseModel,
    ModelCacheConfigType: ModelCacheConfig
](
    ServiceABC[
        RepositoryBaseType,
        ReadSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
        DBCreateSchemaType,
        DBUpdateSchemaType
    ],
    ABC
):
    def __init__(
            self,
            repository: RepositoryBase[Any, DBCreateSchemaType, DBUpdateSchemaType],
            unit_of_work: UnitOfWork,
            table_name: str,
            read_schema_type: type[ReadSchemaType],
            cache: AsyncRedis,
            cache_model_config: ModelCacheConfigType,
    ) -> None:
        super().__init__(
            repository,
            unit_of_work,
            table_name,
            read_schema_type
        )
        self._cache = cache
        self._cache_model_config = cache_model_config

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ReadSchemaType]:
        key = self._cache_model_config.list_key.format(
            table_name=self._table_name,
            skip=skip,
            limit=limit
        )

        if (cached := await self._cache.get(key)) is not None:
            return [self._read_schema_type.model_validate(obj) for obj in orjson.loads(cached)]

        objs = await super().get_all(skip, limit)

        data_to_cache = orjson.dumps(
            [obj.model_dump() for obj in objs]
        )

        await self._cache.set(
            key,
            data_to_cache,
            self._cache_model_config.list_ttl
        )

        return objs

    async def get_by_id(self, obj_id: int) -> ReadSchemaType:
        key = self._cache_model_config.retrieve_key.format(
            table_name=self._table_name,
            obj_id=obj_id
        )

        if (cached := await self._cache.get(key)) is not None:
            return self._read_schema_type.model_validate(orjson.loads(cached))

        obj = await super().get_by_id(obj_id)

        data_to_cache = orjson.dumps(obj.model_dump())

        await self._cache.set(
            key,
            data_to_cache,
            self._cache_model_config.retrieve_ttl
        )

        return obj
