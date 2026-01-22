from asyncpg import exceptions as pg_exc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import MovieShot
from exceptions.db import RelatedObjectNotFoundException
from repositories.base import RepositoryBase
from schemas.movie_shot import MovieShotCreateDB, MovieShotUpdateDB


class MovieShotRepository(RepositoryBase[MovieShot, MovieShotCreateDB, MovieShotUpdateDB]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(MovieShot, session)

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        orig = exc.orig

        if isinstance(orig, pg_exc.ForeignKeyViolationError):
            match getattr(exc.orig, "constraint_name", None):
                case "fk_movie_shots_movie_id_movies":
                    raise RelatedObjectNotFoundException(field_name="movie_id", table_name="movie_shots")
