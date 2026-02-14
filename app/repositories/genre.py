from core.models import Genre
from db_integrity_handler import genres_error_handler
from repositories.signals import SignalRepositoryBase
from schemas.base import Id
from schemas.genre import GenreCreateDB, GenreUpdateDB, GenreCreateEvent, GenreUpdateEvent, genre_event_schemas
from signals.base import Eventer
from signals.event_session import EventSession
from signals.genre import genre_base_publishers


class GenreRepository(
    SignalRepositoryBase[
        Genre,
        GenreCreateDB,
        GenreUpdateDB,
        GenreCreateEvent,
        GenreUpdateEvent,
        Id
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            model=Genre,
            session=session,
            table_error_handler=genres_error_handler,
            eventer=Eventer(publishers=genre_base_publishers),
            event_schemas=genre_event_schemas
        )
