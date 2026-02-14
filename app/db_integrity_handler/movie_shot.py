from constants.db import PostgresErrorCode
from db_integrity_handler.base import TableErrorHandler
from exceptions.db import RelatedObjectNotFoundException
from schemas.db import ConstraintRule

fk_movie_shots_movie_id_movies = ConstraintRule(
    name="fk_movie_shots_movie_id_movies",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="movie_id",
        table_name="movies"
    )
)

movie_shots_error_handler = TableErrorHandler(
    fk_movie_shots_movie_id_movies
)
