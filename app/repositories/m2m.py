from typing import Sequence, Iterable

from sqlalchemy import select, Row
from sqlalchemy.exc import IntegrityError

from core.models import MovieCountryAssociation, MovieGenreAssociation, MoviePersonAssociation
from exceptions.db import UniqueException, RelatedObjectNotFoundException
from repositories.signals import SignalRepositoryBase
from schemas.movie_country import MovieCountryUpdate, MovieCountryCreate, MovieCountryCreateEvent, \
    MovieCountryUpdateEvent, movie_country_event_schemas, MovieCountryDeleteEvent
from schemas.movie_genre import MovieGenreCreate, MovieGenreUpdate, MovieGenreCreateEvent, \
    MovieGenreUpdateEvent, movie_genre_event_schemas, MovieGenreDeleteEvent
from schemas.movie_person import MoviePersonUpdateDB, MoviePersonCreate, MoviePersonCreateEvent, \
    MoviePersonUpdateEvent, movie_person_event_schemas, MoviePersonDeleteEvent
from signals.base import Eventer
from signals.event_session import EventSession
from signals.movie_country import movie_country_base_publishers
from signals.movie_genre import movie_genre_base_publishers
from signals.movie_person import movie_person_base_publishers
from utils import populate_association_map


class MovieCountryRepository(
    SignalRepositoryBase
    [
        MovieCountryAssociation,
        MovieCountryCreate,
        MovieCountryUpdate,
        MovieCountryCreateEvent,
        MovieCountryUpdateEvent,
        MovieCountryDeleteEvent,
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            MovieCountryAssociation,
            session,
            Eventer(movie_country_base_publishers),
            movie_country_event_schemas
        )

    async def get_movie_ids_by_country_id(self, country_id: int) -> Sequence[int]:
        stmt = select(MovieCountryAssociation.movie_id).where(MovieCountryAssociation.country_id == country_id)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_country_ids_by_movie_id(self, movie_id: int) -> Sequence[int]:
        stmt = select(MovieCountryAssociation.country_id).where(MovieCountryAssociation.movie_id == movie_id)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_movie_ids_with_country_ids_by_movie_ids(self, movie_ids: Iterable[int]) -> dict[int, list[int]]:
        if not movie_ids:
            return {}
        result_map: dict[int, list[int]] = {movie_id: [] for movie_id in movie_ids}

        stmt = (
            select(MovieCountryAssociation.movie_id, MovieCountryAssociation.country_id)
            .where(MovieCountryAssociation.movie_id.in_(movie_ids))
        )
        result = await self._session.execute(stmt)
        return populate_association_map(result.all(), result_map)

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
        MovieGenreDeleteEvent,
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            MovieGenreAssociation,
            session,
            Eventer(movie_genre_base_publishers),
            movie_genre_event_schemas
        )

    async def get_movie_ids_by_genre_id(self, genre_id: int) -> Sequence[int]:
        stmt = select(MovieGenreAssociation.movie_id).where(MovieGenreAssociation.genre_id == genre_id)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_genre_ids_by_movie_id(self, movie_id: int) -> Sequence[int]:
        stmt = select(MovieGenreAssociation.genre_id).where(MovieGenreAssociation.movie_id == movie_id)
        result = await self._session.execute(stmt)
        a = result.scalars().all()
        return a

    async def get_movie_ids_with_genre_ids_by_movie_ids(self, movie_ids: Iterable[int]) -> dict[int, list[int]]:
        if not movie_ids:
            return {}
        result_map: dict[int, list[int]] = {movie_id: [] for movie_id in movie_ids}

        stmt = (
            select(MovieGenreAssociation.movie_id, MovieGenreAssociation.genre_id)
            .where(MovieGenreAssociation.movie_id.in_(movie_ids))
        )
        result = await self._session.execute(stmt)
        return populate_association_map(result.all(), result_map)

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
        MoviePersonDeleteEvent,
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            MoviePersonAssociation,
            session,
            Eventer(movie_person_base_publishers),
            movie_person_event_schemas
        )

    async def get_movie_ids_by_person_id(self, person_id: int) -> Sequence[int]:
        stmt = select(MoviePersonAssociation.movie_id).where(MoviePersonAssociation.person_id == person_id)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_person_ids_by_movie_id(self, movie_id: int) -> Sequence[int]:
        stmt = select(MoviePersonAssociation.person_id).where(MoviePersonAssociation.movie_id == movie_id)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_movie_ids_with_person_ids_by_movie_ids(self, movie_ids: Iterable[int]) -> dict[int, list[int]]:
        if not movie_ids:
            return {}
        result_map: dict[int, list[int]] = {movie_id: [] for movie_id in movie_ids}

        stmt = (
            select(MoviePersonAssociation.movie_id, MoviePersonAssociation.person_id)
            .where(MoviePersonAssociation.movie_id.in_(movie_ids))
        )
        result = await self._session.execute(stmt)
        return populate_association_map(result.all(), result_map)

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
