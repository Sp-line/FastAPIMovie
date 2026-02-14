from typing import Sequence, Iterable

from sqlalchemy import select

from core.models import MovieCountryAssociation, MovieGenreAssociation, MoviePersonAssociation
from db_integrity_handler import movie_genre_error_handler, movie_country_error_handler, movie_person_error_handler
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
            model=MovieCountryAssociation,
            session=session,
            table_error_handler=movie_country_error_handler,
            eventer=Eventer(movie_country_base_publishers),
            event_schemas=movie_country_event_schemas
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
            model=MovieGenreAssociation,
            session=session,
            table_error_handler=movie_genre_error_handler,
            eventer=Eventer(movie_genre_base_publishers),
            event_schemas=movie_genre_event_schemas,
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
            model=MoviePersonAssociation,
            session=session,
            table_error_handler=movie_person_error_handler,
            eventer=Eventer(movie_person_base_publishers),
            event_schemas=movie_person_event_schemas
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
