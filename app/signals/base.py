from faststream.nats.publisher.usecase import LogicPublisher
from pydantic import BaseModel

from schemas.event import BaseEventPublishers
from signals.types import AsyncEventFactory


class Eventer[
    TCreateEventSchema: BaseModel,
    TUpdateEventSchema: BaseModel,
    TDeleteEventSchema: BaseModel,
]:
    def __init__(self, publishers: BaseEventPublishers) -> None:
        self.publishers = publishers

    @staticmethod
    def _event_factory[T](publisher: LogicPublisher, payload: T) -> AsyncEventFactory:
        async def factory():
            await publisher.publish(payload)

        return factory

    def create(self, payload: TCreateEventSchema) -> AsyncEventFactory:
        return self._event_factory(self.publishers.create_pub, payload)

    def bulk_create(self, payload: list[TCreateEventSchema]) -> AsyncEventFactory:
        return self._event_factory(self.publishers.bulk_create_pub, payload)

    def update(self, payload: TUpdateEventSchema) -> AsyncEventFactory:
        return self._event_factory(self.publishers.update_pub, payload)

    def delete(self, payload: TDeleteEventSchema) -> AsyncEventFactory:
        return self._event_factory(self.publishers.delete_pub, payload)
