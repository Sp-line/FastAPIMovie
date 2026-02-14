from typing import AsyncGenerator, Sequence

from sqlalchemy import select

from core.models import Person
from db_integrity_handler import persons_error_handler
from repositories.signals import SignalRepositoryBase
from schemas.base import Id
from schemas.person import PersonCreateDB, PersonUpdateDB, PersonCreateEvent, PersonUpdateEvent, person_event_schemas
from signals.base import Eventer
from signals.event_session import EventSession
from signals.person import person_base_publishers


class PersonRepository(
    SignalRepositoryBase[
        Person,
        PersonCreateDB,
        PersonUpdateDB,
        PersonCreateEvent,
        PersonUpdateEvent,
        Id
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            model=Person,
            session=session,
            table_error_handler=persons_error_handler,
            eventer=Eventer(publishers=person_base_publishers),
            event_schemas=person_event_schemas
        )

    async def get_for_elastic_sync_batched(self, batch_size: int = 100) -> AsyncGenerator[Sequence[Person], None]:
        stmt = (
            select(Person)
            .execution_options(yield_per=batch_size)
        )

        result = await self._session.stream_scalars(stmt)

        async for batch in result.partitions(batch_size):
            yield batch
