from abc import abstractmethod, ABC
from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.mixins.int_id_pk import IntIdPkMixin
from schemas.db import IntegrityErrorData


class IntegrityCheckerABC(ABC):
    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        pass

    @staticmethod
    def _get_integrity_error_data(exc: IntegrityError) -> IntegrityErrorData:
        cause = getattr(exc.orig, "__cause__", None)

        sqlstate = str(getattr(exc.orig, "sqlstate", ""))
        constraint = str(getattr(cause, "constraint_name", ""))
        table = str(getattr(cause, "table_name", ""))

        return IntegrityErrorData(
            sqlstate=sqlstate,
            constraint_name=constraint,
            table_name=table,
        )


class RepositoryABC[
    IdT,
    ModelType: IntIdPkMixin,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
](IntegrityCheckerABC, ABC):
    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        self._model = model
        self._session = session

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
            self._handle_integrity_error(e)
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
            self._handle_integrity_error(e)
            raise

        return objs

    @abstractmethod
    async def get_by_id(self, obj_id: IdT) -> ModelType | None:
        ...

    @abstractmethod
    async def update(self, obj_id: IdT, data: UpdateSchemaType) -> ModelType | None:
        ...

    @abstractmethod
    async def delete(self, obj_id: IdT) -> bool:
        ...