from sqlalchemy.exc import IntegrityError

from core.models import Genre
from exceptions.db import UniqueFieldException, DeleteConstraintException
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
            Genre,
            session,
            Eventer(publishers=genre_base_publishers),
            genre_event_schemas
        )

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        err_data = self._get_integrity_error_data(exc)

        match err_data.sqlstate:
            case "23505":
                match err_data.constraint_name:
                    case "uq_genres_name":
                        raise UniqueFieldException(field_name="name", table_name=err_data.table_name)
                    case "uq_genres_slug":
                        raise UniqueFieldException(field_name="slug", table_name=err_data.table_name)
            case "23001":
                match err_data.constraint_name:
                    case "fk_movie_genre_associations_genre_id_genres":
                        raise DeleteConstraintException(
                            table_name=err_data.table_name,
                            referencing_table="movies"
                        )
