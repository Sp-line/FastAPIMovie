from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import MovieShot
from exceptions.db import RelatedObjectNotFoundException
from repositories.base import IntRepositoryBase
from schemas.movie_shot import MovieShotCreateDB, MovieShotUpdateDB


class MovieShotRepository(IntRepositoryBase[MovieShot, MovieShotCreateDB, MovieShotUpdateDB]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(MovieShot, session)

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        err_data = self._get_integrity_error_data(exc)

        match err_data.sqlstate:
            case "23503":
                match err_data.constraint_name:
                    case "fk_movie_shots_movie_id_movies":
                        raise RelatedObjectNotFoundException(field_name="movie_id", table_name="movies")
