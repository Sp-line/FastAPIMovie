from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Genre
from exceptions.db import UniqueFieldException, DeleteConstraintException
from repositories.base import IntRepositoryBase
from schemas.genre import GenreCreateDB, GenreUpdateDB


class GenreRepository(IntRepositoryBase[Genre, GenreCreateDB, GenreUpdateDB]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Genre, session)

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        err_data = self._get_integrity_error_data(exc)

        match err_data.sqlstate:
            case "23505":
                match err_data.constraint_name:
                    case "uq_genres_name":
                        raise UniqueFieldException(field_name="name", table_name=err_data.table_name)
                    case "uq_genres_slug":
                        raise UniqueFieldException(field_name="slug", table_name=err_data.table_name)
            case "23001":
                match err_data.constraint_name:
                    case "fk_movie_genre_associations_genre_id_genres":
                        raise DeleteConstraintException(
                            table_name=err_data.table_name,
                            referencing_table="movies"
                        )
