from typing import Any

from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.elements import BinaryExpression

from core.models.mixins.int_id_pk import IntIdPkMixin
from repositories.abc import RepositoryABC
from schemas.m2m import CompositeIdBase


class IntRepositoryBase[
    ModelType: IntIdPkMixin,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
](
    RepositoryABC[int, ModelType, CreateSchemaType, UpdateSchemaType]
):
    async def get_by_id(self, obj_id: int) -> ModelType | None:
        return await self._session.get(self._model, obj_id)

    async def update(self, obj_id: int, data: UpdateSchemaType) -> ModelType | None:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_by_id(obj_id)

        stmt = (
            update(self._model)
            .where(self._model.id == obj_id)
            .values(**update_data)
            .returning(self._model)
        )

        try:
            result = await self._session.execute(stmt)
        except IntegrityError as e:
            self._handle_integrity_error(e)
            raise

        return result.scalar_one_or_none()

    async def delete(self, obj_id: int) -> bool:
        stmt = delete(self._model).where(self._model.id == obj_id)

        try:
            result = await self._session.execute(stmt)
        except IntegrityError as e:
            self._handle_integrity_error(e)
            raise

        return result.rowcount > 0  # type: ignore


class M2MRepositoryBase[
    ModelType: IntIdPkMixin,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
    CompositeIdSchemaType: CompositeIdBase,
](
    RepositoryABC[CompositeIdSchemaType, ModelType, CreateSchemaType, UpdateSchemaType],
):
    def _get_composite_id_conditions(self, obj_id: CompositeIdSchemaType) -> list[BinaryExpression[Any]]:
        pk_data = obj_id.model_dump()

        return [
            getattr(self._model, key) == value
            for key, value in pk_data.items()
        ]

    async def get_by_id(self, obj_id: CompositeIdSchemaType) -> ModelType | None:
        stmt = select(self._model).where(*self._get_composite_id_conditions(obj_id))

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, obj_id: CompositeIdSchemaType, data: UpdateSchemaType) -> ModelType | None:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_by_id(obj_id)

        stmt = (
            update(self._model)
            .where(*self._get_composite_id_conditions(obj_id))
            .values(**update_data)
            .returning(self._model)
        )

        try:
            result = await self._session.execute(stmt)
        except IntegrityError as e:
            self._handle_integrity_error(e)
            raise

        return result.scalar_one_or_none()

    async def delete(self, obj_id: CompositeIdSchemaType) -> bool:
        stmt = delete(self._model).where(*self._get_composite_id_conditions(obj_id))

        try:
            result = await self._session.execute(stmt)
        except IntegrityError as e:
            self._handle_integrity_error(e)
            raise

        return result.rowcount > 0  # type: ignore
