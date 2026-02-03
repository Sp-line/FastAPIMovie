from sqlalchemy.exc import IntegrityError

from core.models import MovieCountryAssociation, MovieGenreAssociation, MoviePersonAssociation
from exceptions.db import UniqueException, RelatedObjectNotFoundException
from repositories.signals import SignalRepositoryBase
from schemas.base import Id
from schemas.movie_country import MovieCountryUpdate, MovieCountryCreate, MovieCountryCreateEvent, \
    MovieCountryUpdateEvent, movie_country_event_schemas
from schemas.movie_genre import MovieGenreCreate, MovieGenreUpdate, MovieGenreCreateEvent, \
    MovieGenreUpdateEvent, movie_genre_event_schemas
from schemas.movie_person import MoviePersonUpdateDB, MoviePersonCreate, MoviePersonCreateEvent, \
    MoviePersonUpdateEvent, movie_person_event_schemas
from signals.base import Eventer
from signals.event_session import EventSession
from signals.movie_country import movie_country_base_publishers
from signals.movie_genre import movie_genre_base_publishers
from signals.movie_person import movie_person_base_publishers


class MovieCountryRepository(
    SignalRepositoryBase
    [
        MovieCountryAssociation,
        MovieCountryCreate,
        MovieCountryUpdate,
        MovieCountryCreateEvent,
        MovieCountryUpdateEvent,
        Id,
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            MovieCountryAssociation,
            session,
            Eventer(movie_country_base_publishers),
            movie_country_event_schemas
        )

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        err_data = self._get_integrity_error_data(exc)

        match err_data.sqlstate:
            case "23505":
                match err_data.constraint_name:
                    case "uq_country_movie":
                        raise UniqueException(err_data.table_name, "country_id", "movie_id")
            case "23503":
                match err_data.constraint_name:
                    case "fk_movie_country_associations_country_id_countries":
                        raise RelatedObjectNotFoundException(
                            field_name="country_id",
                            table_name="countries",
                        )
                    case "fk_movie_country_associations_movie_id_movies":
                        raise RelatedObjectNotFoundException(
                            field_name="movie_id",
                            table_name="movies"
                        )


class MovieGenreRepository(
    SignalRepositoryBase
    [
        MovieGenreAssociation,
        MovieGenreCreate,
        MovieGenreUpdate,
        MovieGenreCreateEvent,
        MovieGenreUpdateEvent,
        Id,
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            MovieGenreAssociation,
            session,
            Eventer(movie_genre_base_publishers),
            movie_genre_event_schemas
        )

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        err_data = self._get_integrity_error_data(exc)

        match err_data.sqlstate:
            case "23505":
                match err_data.constraint_name:
                    case "uq_movie_genre":
                        raise UniqueException(err_data.table_name, "genre_id", "movie_id")
            case "23503":
                match err_data.constraint_name:
                    case "fk_movie_genre_associations_genre_id_genres":
                        raise RelatedObjectNotFoundException(
                            field_name="genre_id",
                            table_name="genres",
                        )
                    case "fk_movie_genre_associations_movie_id_movies":
                        raise RelatedObjectNotFoundException(
                            field_name="movie_id",
                            table_name="movies"
                        )


class MoviePersonRepository(
    SignalRepositoryBase
    [
        MoviePersonAssociation,
        MoviePersonCreate,
        MoviePersonUpdateDB,
        MoviePersonCreateEvent,
        MoviePersonUpdateEvent,
        Id,
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            MoviePersonAssociation,
            session,
            Eventer(movie_person_base_publishers),
            movie_person_event_schemas
        )

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        err_data = self._get_integrity_error_data(exc)

        match err_data.sqlstate:
            case "23505":
                match err_data.constraint_name:
                    case "uq_movie_person_role":
                        raise UniqueException(err_data.table_name, "person_id", "movie_id", "role")
            case "23503":
                match err_data.constraint_name:
                    case "fk_movie_person_associations_person_id_persons":
                        raise RelatedObjectNotFoundException(
                            field_name="person_id",
                            table_name="persons",
                        )
                    case "fk_movie_person_associations_movie_id_movies":
                        raise RelatedObjectNotFoundException(
                            field_name="movie_id",
                            table_name="movies"
                        )
