from abc import ABC

from pydantic import BaseModel

from core.models.mixins.int_id_pk import IntIdPkMixin
from repositories.base import RepositoryBase
from repositories.unit_of_work import UnitOfWork
from schemas.base import Id
from schemas.event import EventSchemas
from signals.base import Eventer
from signals.event_session import EventSession


class SignalRepositoryBase[
    TModel: IntIdPkMixin,
    TCreateSchema: BaseModel,
    TUpdateSchema: BaseModel,
    TCreateEventSchema: BaseModel,
    TUpdateEventSchema: BaseModel,
    TDeleteEventSchema: Id,
](
    RepositoryBase[
        TModel,
        TCreateSchema,
        TUpdateSchema,
    ],
    ABC
):
    def __init__(
            self,
            model: type[TModel],
            session: EventSession,
            eventer: Eventer,
            event_schemas: EventSchemas[
                TCreateEventSchema,
                TUpdateEventSchema,
                TDeleteEventSchema
            ]
    ) -> None:
        super().__init__(model, session)
        self._eventer = eventer
        self.event_schemas = event_schemas

    async def create(self, obj: TCreateSchema) -> TModel:
        model = await super().create(obj)
        self._session.events.append(
            self._eventer.create(self.event_schemas.create.model_validate(model))
        )
        return model

    async def bulk_create(self, objs: list[TCreateSchema]) -> list[TModel]:
        models = await super().bulk_create(objs)
        self._session.events.append(
            self._eventer.bulk_create(
                [self.event_schemas.create.model_validate(model) for model in models],
            )
        )
        return models

    async def update(self, obj_id: int, obj: TUpdateSchema) -> TModel | None:
        model = await super().update(obj_id, obj)
        if model:
            self._session.events.append(
                self._eventer.update(
                    self.event_schemas.update.model_validate(model)
                )
            )
        return model

    async def delete(self, obj_id: int) -> bool:
        if deleted := await super().delete(obj_id):
            self._session.events.append(
                self._eventer.delete(
                    self.event_schemas.delete(id=obj_id)
                )
            )
        return deleted


class SignalUnitOfWork(UnitOfWork):
    async def __aexit__(
            self,
            exc_type: object | None,
            exc_val: BaseException | None,
            exc_tb: object | None,
    ) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        if exc_type is None:
            await self._session.events.send_all()


