from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from core.models.mixins.int_id_pk import IntIdPkMixin
from db_integrity_handler.base import TableErrorHandler
from signals.event_session import EventSession


class RepositoryBase[
    ModelType: IntIdPkMixin,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
]:
    def __init__(
            self,
            model: type[ModelType],
            session: EventSession,
            table_error_handler: TableErrorHandler
    ) -> None:
        self._model = model
        self._session = session
        self._table_error_handler = table_error_handler

    async def get_all(
            self,
            skip: int = 0,
            limit: int = 100,
    ) -> Sequence[ModelType]:
        stmt = select(self._model).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def create(self, data: CreateSchemaType) -> ModelType:
        obj = self._model(**data.model_dump())
        self._session.add(obj)

        try:
            await self._session.flush()
        except IntegrityError as e:
            self._table_error_handler.handle(e)
            raise

        await self._session.refresh(obj)
        return obj

    async def bulk_create(self, data: list[CreateSchemaType]) -> list[ModelType]:
        if not data:
            return []

        objs = [
            self._model(**item.model_dump())
            for item in data
        ]

        self._session.add_all(objs)

        try:
            await self._session.flush()
        except IntegrityError as e:
            self._table_error_handler.handle(e)
            raise

        return objs

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
            self._table_error_handler.handle(e)
            raise

        return result.scalar_one_or_none()

    async def delete(self, obj_id: int) -> bool:
        stmt = delete(self._model).where(self._model.id == obj_id)

        try:
            result = await self._session.execute(stmt)
        except IntegrityError as e:
            self._table_error_handler.handle(e)
            raise

        return result.rowcount > 0  # type: ignore
