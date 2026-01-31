from abc import ABC
from typing import Any

import orjson
from pydantic import BaseModel
from redis.asyncio.client import Redis as AsyncRedis

from repositories.abc import RepositoryABC
from repositories.base import IntRepositoryBase, M2MRepositoryBase
from repositories.unit_of_work import UnitOfWork
from schemas.cache import ModelCacheConfig
from schemas.m2m import CompositeIdBase
from services.abc import ServiceABC


class CacheServiceABC[
    IdT,
    RepositoryBaseType: RepositoryABC,
    ReadSchemaType: BaseModel,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
    DBCreateSchemaType: BaseModel,
    DBUpdateSchemaType: BaseModel,
    ModelCacheConfigType: ModelCacheConfig
](
    ServiceABC[
        IdT,
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
            repository: RepositoryABC[IdT, Any, DBCreateSchemaType, DBUpdateSchemaType],
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

    async def get_by_id(self, obj_id: IdT) -> ReadSchemaType:
        key = self._cache_model_config.retrieve_key.format(
            table_name=self._table_name,
            obj_id=self._prepare_id_for_generate_cache_key(obj_id)
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

    @staticmethod
    def _prepare_id_for_generate_cache_key(obj_id: IdT) -> str:
        return str(obj_id)


class IntCacheServiceABC[
    IntRepositoryBaseType: IntRepositoryBase,
    ReadSchemaType: BaseModel,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
    DBCreateSchemaType: BaseModel,
    DBUpdateSchemaType: BaseModel,
    ModelCacheConfigType: ModelCacheConfig
](
    CacheServiceABC[
        int,
        IntRepositoryBaseType,
        ReadSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
        DBCreateSchemaType,
        DBUpdateSchemaType,
        ModelCacheConfigType
    ],
    ABC
):
    pass


class M2MCacheServiceABC[
    M2MRepositoryBaseType: M2MRepositoryBase,
    ReadSchemaType: BaseModel,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
    CompositeIdSchemaType: CompositeIdBase,
    DBCreateSchemaType: BaseModel,
    DBUpdateSchemaType: BaseModel,
    ModelCacheConfigType: ModelCacheConfig
](
    CacheServiceABC[
        CompositeIdSchemaType,
        M2MRepositoryBaseType,
        ReadSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
        DBCreateSchemaType,
        DBUpdateSchemaType,
        ModelCacheConfigType
    ],
    ABC
):
    pass
