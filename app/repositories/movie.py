from typing import Sequence, AsyncGenerator

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import load_only, selectinload

from core.models import Movie, MoviePersonAssociation, Genre, Country, MovieCountryAssociation, MovieGenreAssociation
from exceptions.db import UniqueFieldException
from repositories.signals import SignalRepositoryBase
from schemas.base import Id
from schemas.movie import MovieCreateDB, MovieUpdateDB, MovieCreateEvent, MovieUpdateEvent, movie_event_schemas
from signals.base import Eventer
from signals.event_session import EventSession
from signals.movie import movie_base_publishers


class MovieRepository(
    SignalRepositoryBase[
        Movie,
        MovieCreateDB,
        MovieUpdateDB,
        MovieCreateEvent,
        MovieUpdateEvent,
        Id
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            Movie,
            session,
            Eventer(movie_base_publishers),
            movie_event_schemas
        )

    async def get_for_list(
            self,
            skip: int = 0,
            limit: int = 100,
    ) -> Sequence[Movie]:
        stmt = (
            select(Movie)
            .options(
                load_only(
                    Movie.id,
                    Movie.title,
                    Movie.slug,
                    Movie.duration,
                    Movie.release_year,
                    Movie.poster_url,
                    Movie.age_rating,
                ),
                selectinload(Movie.genres)
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_for_detail(self, movie_id: int) -> Movie | None:
        stmt = (
            select(Movie)
            .where(Movie.id == movie_id)
            .options(
                selectinload(Movie.genre_associations).joinedload(MovieGenreAssociation.genre),
                selectinload(Movie.country_associations).joinedload(MovieCountryAssociation.country),
                selectinload(Movie.person_associations).joinedload(MoviePersonAssociation.person),
                selectinload(Movie.shots),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_for_elastic_sync_batched(self, batch_size: int = 50) -> AsyncGenerator[Sequence[Movie], None]:
        stmt = (
            select(Movie)
            .options(
                selectinload(Movie.genre_associations).load_only(MovieGenreAssociation.genre_id),
                selectinload(Movie.country_associations).load_only(MovieCountryAssociation.country_id),
                selectinload(Movie.person_associations).load_only(MoviePersonAssociation.person_id)
            )
            .execution_options(yield_per=batch_size)
        )
        result = await self._session.stream_scalars(stmt)

        async for batch in result.partitions(batch_size):
            yield batch

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        err_data = self._get_integrity_error_data(exc)

        match err_data.sqlstate:
            case "23505":
                match err_data.constraint_name:
                    case "uq_movies_slug":
                        raise UniqueFieldException(field_name="slug", table_name=err_data.table_name)
