from asyncpg import exceptions as pg_exc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import MovieCountryAssociation, MovieGenreAssociation, MoviePersonAssociation
from exceptions.db import UniqueException, RelatedObjectNotFoundException
from repositories.base import M2MRepositoryBase
from schemas.movie_country import MovieCountryUpdate, MovieCountryCreate, MovieCountryCompositeId
from schemas.movie_genre import MovieGenreCreate, MovieGenreUpdate, MovieGenreCompositeId
from schemas.movie_person import MoviePersonUpdate, MoviePersonCreate, MoviePersonCompositeId


class MovieCountryRepository(
    M2MRepositoryBase
    [
        MovieCountryAssociation,
        MovieCountryCreate,
        MovieCountryUpdate,
        MovieCountryCompositeId
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(MovieCountryAssociation, session)

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        orig = exc.orig

        if isinstance(orig, pg_exc.UniqueViolationError):
            match getattr(orig, "constraint_name", None):
                case "uq_country_movie":
                    raise UniqueException("movie_country_associations", "country_id", "movie_id")
        elif isinstance(orig, pg_exc.ForeignKeyViolationError):
            match getattr(orig, "constraint_name", None):
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
    M2MRepositoryBase
    [
        MovieGenreAssociation,
        MovieGenreCreate,
        MovieGenreUpdate,
        MovieGenreCompositeId
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(MovieGenreAssociation, session)

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        orig = exc.orig

        if isinstance(orig, pg_exc.UniqueViolationError):
            match getattr(orig, "constraint_name", None):
                case "uq_movie_genre":
                    raise UniqueException("movie_genre_associations", "genre_id", "movie_id")
        elif isinstance(orig, pg_exc.ForeignKeyViolationError):
            match getattr(orig, "constraint_name", None):
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
    M2MRepositoryBase
    [
        MoviePersonAssociation,
        MoviePersonCreate,
        MoviePersonUpdate,
        MoviePersonCompositeId
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(MoviePersonAssociation, session)

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        orig = exc.orig

        if isinstance(orig, pg_exc.UniqueViolationError):
            match getattr(orig, "constraint_name", None):
                case "uq_movie_person_role":
                    raise UniqueException("movie_person_associations", "person_id", "movie_id", "role")
        elif isinstance(orig, pg_exc.ForeignKeyViolationError):
            match getattr(orig, "constraint_name", None):
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
