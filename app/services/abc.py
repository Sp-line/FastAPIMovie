from abc import ABC, abstractmethod
from typing import Any, cast

from pydantic import BaseModel

from exceptions.db import ObjectNotFoundException
from repositories.base import RepositoryBase
from repositories.unit_of_work import UnitOfWork


class ServiceABC[
    RepositoryBaseType: RepositoryBase,
    ReadSchemaType: BaseModel,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
    DBCreateSchemaType: BaseModel,
    DBUpdateSchemaType: BaseModel,
](ABC):
    def __init__(
            self,
            repository: RepositoryBase[Any, DBCreateSchemaType, DBUpdateSchemaType],
            unit_of_work: UnitOfWork,
            table_name: str,
            read_schema_type: type[ReadSchemaType],
    ) -> None:
        self._repository = cast(RepositoryBaseType, repository)
        self._uof = unit_of_work
        self._table_name = table_name
        self._read_schema_type = read_schema_type

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ReadSchemaType]:
        return [self._read_schema_type.model_validate(obj) for obj in await self._repository.get_all(skip, limit)]

    async def bulk_create(self, data: list[CreateSchemaType]) -> list[ReadSchemaType]:
        prepared_data = list(map(self._prepare_create_data, data))
        async with self._uof:
            return [self._read_schema_type.model_validate(obj) for obj in await self._repository.bulk_create(prepared_data)]

    async def create(self, data: CreateSchemaType) -> ReadSchemaType:
        prepared_data = self._prepare_create_data(data)
        async with self._uof:
            return self._read_schema_type.model_validate(await self._repository.create(prepared_data))

    async def get_by_id(self, obj_id: int) -> ReadSchemaType:
        if not (obj := await self._repository.get_by_id(obj_id)):
            raise ObjectNotFoundException(obj_id, self._table_name)
        return self._read_schema_type.model_validate(obj)

    async def update(self, obj_id: int, data: UpdateSchemaType) -> ReadSchemaType:
        prepared_data = self._prepare_update_data(data)
        async with self._uof:
            new_obj = await self._repository.update(obj_id, prepared_data)
            if not new_obj:
                raise ObjectNotFoundException(obj_id, self._table_name)
            return self._read_schema_type.model_validate(new_obj)

    async def delete(self, obj_id: int) -> None:
        async with self._uof:
            if not await self._repository.delete(obj_id):
                raise ObjectNotFoundException(obj_id, self._table_name)

    @staticmethod
    @abstractmethod
    def _prepare_create_data(data: CreateSchemaType) -> DBCreateSchemaType:
        ...

    @staticmethod
    @abstractmethod
    def _prepare_update_data(data: UpdateSchemaType) -> DBUpdateSchemaType:
        ...
