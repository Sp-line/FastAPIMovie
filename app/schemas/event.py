from faststream.nats.publisher.usecase import LogicPublisher
from pydantic import BaseModel, ConfigDict

from schemas.base import Id


class BaseEventPublishers(BaseModel):
    create_pub: LogicPublisher
    bulk_create_pub: LogicPublisher
    update_pub: LogicPublisher
    delete_pub: LogicPublisher

    model_config = ConfigDict(arbitrary_types_allowed=True)


class EventSchemas[
    TCreateEventSchema: BaseModel,
    TUpdateEventSchema: BaseModel,
    TDeleteEventSchema: Id,
](BaseModel):
    create: type[TCreateEventSchema]
    update: type[TUpdateEventSchema]
    delete: type[TDeleteEventSchema]

    model_config = ConfigDict(arbitrary_types_allowed=True)
