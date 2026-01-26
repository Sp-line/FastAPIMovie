from abc import ABC

from pydantic import BaseModel

from exceptions.db import ObjectNotFoundException
from repositories.base import RepositoryABC
from repositories.unit_of_work import UnitOfWork


class ServiceABC[
    IdT,
    RepositoryBaseType: RepositoryABC,
    ReadSchemaType: BaseModel,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
](ABC):
    def __init__(
            self,
            repository: RepositoryBaseType,
            unit_of_work: UnitOfWork,
            table_name: str,
            read_schema_type: type[BaseModel],
    ) -> None:
        self._repository = repository
        self._uof = unit_of_work
        self._table_name = table_name
        self._read_schema_type = read_schema_type

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ReadSchemaType]:
        return [self._read_schema_type.model_validate(obj) for obj in await self._repository.get_all(skip, limit)]

    async def bulk_create(self, data: list[CreateSchemaType]) -> list[ReadSchemaType]:
        data = list(map(self._prepare_create_data, data))
        async with self._uof:
            return [self._read_schema_type.model_validate(obj) for obj in await self._repository.bulk_create(data)]

    async def create(self, data: CreateSchemaType) -> ReadSchemaType:
        prepared_data = self._prepare_create_data(data)
        async with self._uof:
            return self._read_schema_type.model_validate(await self._repository.create(prepared_data))

    async def get_by_id(self, obj_id: IdT) -> ReadSchemaType:
        if not (obj := await self._repository.get_by_id(obj_id)):
            raise ObjectNotFoundException[IdT](obj_id, self._table_name)
        return self._read_schema_type.model_validate(obj)

    async def update(self, obj_id: IdT, data: UpdateSchemaType) -> ReadSchemaType:
        prepared_data = self._prepare_update_data(data)
        async with self._uof:
            new_obj = await self._repository.update(obj_id, prepared_data)
            if not new_obj:
                raise ObjectNotFoundException[IdT](obj_id, self._table_name)
            return self._read_schema_type.model_validate(new_obj)

    async def delete(self, obj_id: IdT) -> None:
        async with self._uof:
            if not await self._repository.delete(obj_id):
                raise ObjectNotFoundException[IdT](obj_id, self._table_name)

    @staticmethod
    def _prepare_create_data(data: CreateSchemaType) -> CreateSchemaType | BaseModel:
        return data

    @staticmethod
    def _prepare_update_data(data: UpdateSchemaType) -> UpdateSchemaType | BaseModel:
        return data
