from asyncpg import exceptions as pg_exc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Genre
from exceptions.db import UniqueFieldException, DeleteConstraintException
from repositories.base import RepositoryBase
from schemas.genre import GenreCreateDB, GenreUpdateDB


class GenreRepository(RepositoryBase[Genre, GenreCreateDB, GenreUpdateDB]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Genre, session)

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        orig = exc.orig

        if isinstance(orig, pg_exc.UniqueViolationError):
            match getattr(exc.orig, "constraint_name", None):
                case "uq_genres_name":
                    raise UniqueFieldException(field_name="name", table_name="genres")
                case "uq_genres_slug":
                    raise UniqueFieldException(field_name="slug", table_name="genres")
        elif isinstance(orig, pg_exc.ForeignKeyViolationError):
            match getattr(orig, "constraint_name", None):
                case "fk_movie_genre_associations_genre_id_genres":
                    raise DeleteConstraintException(
                        table_name="genres",
                        referencing_table="movies"
                    )