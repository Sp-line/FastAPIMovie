from sqlalchemy.exc import IntegrityError

from core.models import MovieShot
from exceptions.db import RelatedObjectNotFoundException
from repositories.signals import SignalRepositoryBase
from schemas.base import Id
from schemas.movie_shot import MovieShotCreateDB, MovieShotUpdateDB, MovieShotCreateEvent, MovieShotUpdateEvent, \
    movie_shot_event_schemas
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
        Id,
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            MovieShot,
            session,
            Eventer(movie_shot_base_publishers),
            movie_shot_event_schemas
        )

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        err_data = self._get_integrity_error_data(exc)

        match err_data.sqlstate:
            case "23503":
                match err_data.constraint_name:
                    case "fk_movie_shots_movie_id_movies":
                        raise RelatedObjectNotFoundException(field_name="movie_id", table_name="movies")
