from typing import Generic, Type

from pydantic import BaseModel

from app_types.repositories import RepositoryBaseType, M2MRepositoryBaseType
from app_types.schemas import ReadSchemaType, CreateSchemaType, UpdateSchemaType, CompositeIdSchemaType
from exceptions.db import ObjectNotFoundException
from repositories.unit_of_work import UnitOfWork


class ServiceBase(Generic[RepositoryBaseType, ReadSchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
            self,
            repository: RepositoryBaseType,
            unit_of_work: UnitOfWork,
            table_name: str,
            read_schema_type: Type[BaseModel],
    ) -> None:
        self._repository = repository
        self._uof = unit_of_work
        self._table_name = table_name
        self._read_schema_type = read_schema_type

    async def get_all(self) -> list[ReadSchemaType]:
        return [self._read_schema_type.model_validate(obj) for obj in await self._repository.get_all()]

    async def get_by_id(self, obj_id: int) -> ReadSchemaType:
        if not (obj := await self._repository.get_by_id(obj_id)):
            raise ObjectNotFoundException(obj_id, self._table_name)
        return self._read_schema_type.model_validate(obj)

    async def bulk_create(self, data: list[CreateSchemaType]) -> list[ReadSchemaType]:
        data = list(map(self._prepare_create_data, data))
        async with self._uof:
            return [self._read_schema_type.model_validate(obj) for obj in await self._repository.bulk_create(data)]

    async def create(self, data: CreateSchemaType) -> ReadSchemaType:
        prepared_data = self._prepare_create_data(data)
        async with self._uof:
            return self._read_schema_type.model_validate(await self._repository.create(prepared_data))

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

    def _prepare_create_data(self, data: CreateSchemaType) -> CreateSchemaType | BaseModel:
        return data

    def _prepare_update_data(self, data: UpdateSchemaType) -> UpdateSchemaType | BaseModel:
        return data


class M2MServiceBase(
    ServiceBase[M2MRepositoryBaseType, ReadSchemaType, CreateSchemaType, UpdateSchemaType],
    Generic[M2MRepositoryBaseType, ReadSchemaType, CreateSchemaType, UpdateSchemaType, CompositeIdSchemaType],
):
    def __init__(
            self,
            repository: RepositoryBaseType,
            unit_of_work: UnitOfWork,
            table_name: str,
            read_schema_type: Type[BaseModel],
    ) -> None:
        super().__init__(
            repository,
            unit_of_work,
            table_name,
            read_schema_type,
        )

    async def get_by_id(self, obj_id: CompositeIdSchemaType) -> ReadSchemaType:
        if not (obj := await self._repository.get_by_id(obj_id)):
            raise ObjectNotFoundException(obj_id, self._table_name)
        return self._read_schema_type.model_validate(obj)

    async def update(self, obj_id: CompositeIdSchemaType, data: UpdateSchemaType) -> ReadSchemaType:
        prepared_data = self._prepare_update_data(data)
        async with self._uof:
            new_obj = await self._repository.update(obj_id, prepared_data)
            if not new_obj:
                raise ObjectNotFoundException(obj_id, self._table_name)
            return self._read_schema_type.model_validate(new_obj)

    async def delete(self, obj_id: CompositeIdSchemaType) -> None:
        async with self._uof:
            if not await self._repository.delete(obj_id):
                raise ObjectNotFoundException(obj_id, self._table_name)
