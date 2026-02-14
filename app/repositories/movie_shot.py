from core.models import MovieShot
from db_integrity_handler import movie_shots_error_handler
from repositories.signals import SignalRepositoryBase
from schemas.movie_shot import MovieShotCreateDB, MovieShotUpdateDB, MovieShotCreateEvent, MovieShotUpdateEvent, \
    movie_shot_event_schemas, MovieShotDeleteEvent
from signals.base import Eventer
from signals.event_session import EventSession
from signals.movie_shot import movie_shot_base_publishers


class MovieShotRepository(
    SignalRepositoryBase[
        MovieShot,
        MovieShotCreateDB,
        MovieShotUpdateDB,
        MovieShotCreateEvent,
        MovieShotUpdateEvent,
        MovieShotDeleteEvent,
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            model=MovieShot,
            session=session,
            table_error_handler=movie_shots_error_handler,
            eventer=Eventer(movie_shot_base_publishers),
            event_schemas=movie_shot_event_schemas
        )
