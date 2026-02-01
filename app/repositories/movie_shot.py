from sqlalchemy.exc import IntegrityError

from core.models import MovieShot
from exceptions.db import RelatedObjectNotFoundException
from repositories.base import RepositoryBase
from schemas.movie_shot import MovieShotCreateDB, MovieShotUpdateDB
from signals.event_session import EventSession


class MovieShotRepository(RepositoryBase[MovieShot, MovieShotCreateDB, MovieShotUpdateDB]):
    def __init__(self, session: EventSession) -> None:
        super().__init__(MovieShot, session)

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        err_data = self._get_integrity_error_data(exc)

        match err_data.sqlstate:
            case "23503":
                match err_data.constraint_name:
                    case "fk_movie_shots_movie_id_movies":
                        raise RelatedObjectNotFoundException(field_name="movie_id", table_name="movies")
