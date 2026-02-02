from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import load_only, selectinload

from core.models import Movie, MoviePersonAssociation
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
                selectinload(Movie.genres),
                selectinload(Movie.countries),
                selectinload(Movie.shots),
                selectinload(Movie.person_associations).joinedload(MoviePersonAssociation.person)
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        err_data = self._get_integrity_error_data(exc)

        match err_data.sqlstate:
            case "23505":
                match err_data.constraint_name:
                    case "uq_movies_slug":
                        raise UniqueFieldException(field_name="slug", table_name=err_data.table_name)
