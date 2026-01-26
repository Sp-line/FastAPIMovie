from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, selectinload

from core.models import Movie, MoviePersonAssociation
from exceptions.db import UniqueFieldException
from repositories.base import IntRepositoryBase
from schemas.movie import MovieCreateDB, MovieUpdateDB


class MovieRepository(IntRepositoryBase[Movie, MovieCreateDB, MovieUpdateDB]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Movie, session)

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

    async def get_for_read(self, movie_id: int) -> Movie:
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
