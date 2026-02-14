from core.models import Country
from db_integrity_handler import countries_error_handler
from repositories.signals import SignalRepositoryBase
from schemas.base import Id
from schemas.country import CountryCreateDB, CountryUpdateDB, CountryCreateEvent, CountryUpdateEvent, \
    country_event_schemas
from signals.base import Eventer
from signals.country import country_base_publishers
from signals.event_session import EventSession


class CountryRepository(
    SignalRepositoryBase[
        Country,
        CountryCreateDB,
        CountryUpdateDB,
        CountryCreateEvent,
        CountryUpdateEvent,
        Id
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            model=Country,
            session=session,
            table_error_handler=countries_error_handler,
            eventer=Eventer(publishers=country_base_publishers),
            event_schemas=country_event_schemas
        )
