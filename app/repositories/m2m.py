from sqlalchemy.exc import IntegrityError

from core.models import MovieCountryAssociation, MovieGenreAssociation, MoviePersonAssociation
from exceptions.db import UniqueException, RelatedObjectNotFoundException
from repositories.base import RepositoryBase
from schemas.movie_country import MovieCountryUpdate, MovieCountryCreate, MovieCountryCompositeId
from schemas.movie_genre import MovieGenreCreate, MovieGenreUpdate, MovieGenreCompositeId
from schemas.movie_person import MoviePersonUpdate, MoviePersonCreate, MoviePersonCompositeId
from signals.event_session import EventSession


class MovieCountryRepository(
    RepositoryBase
    [
        MovieCountryAssociation,
        MovieCountryCreate,
        MovieCountryUpdate,
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(MovieCountryAssociation, session)

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
    RepositoryBase
    [
        MovieGenreAssociation,
        MovieGenreCreate,
        MovieGenreUpdate,
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(MovieGenreAssociation, session)

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
    RepositoryBase
    [
        MoviePersonAssociation,
        MoviePersonCreate,
        MoviePersonUpdate,
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(MoviePersonAssociation, session)

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
