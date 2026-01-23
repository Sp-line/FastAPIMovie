from typing import Generic, Type, Sequence, Any

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BinaryExpression

from app_types.models import ModelType
from app_types.schemas import CreateSchemaType, UpdateSchemaType, CompositeIdSchemaType
from schemas.db import IntegrityErrorData


class RepositoryBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
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

    async def get_by_id(self, obj_id: int) -> ModelType | None:
        return await self._session.get(self._model, obj_id)

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

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        pass

    @staticmethod
    def _get_integrity_error_data(exc: IntegrityError) -> IntegrityErrorData:
        return IntegrityErrorData(
            sqlstate=getattr(exc.orig, "sqlstate", None),
            constraint_name = getattr(exc.orig.__cause__, "constraint_name", None),
            table_name = getattr(exc.orig.__cause__, "table_name", None),
        )


class M2MRepositoryBase(
    RepositoryBase[ModelType, CreateSchemaType, UpdateSchemaType],
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, CompositeIdSchemaType]
):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        super().__init__(model, session)

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
