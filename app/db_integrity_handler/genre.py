from constants.db import PostgresErrorCode
from db_integrity_handler.base import TableErrorHandler
from exceptions.db import UniqueFieldException, DeleteConstraintException
from schemas.db import ConstraintRule

uq_genres_name = ConstraintRule(
    name="uq_genres_name",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="name",
        table_name="genres"
    )
)

uq_genres_slug = ConstraintRule(
    name="uq_genres_slug",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="slug",
        table_name="genres"
    )
)

fk_movie_genre_associations_genre_id_genres = ConstraintRule(
    name="fk_movie_genre_associations_genre_id_genres",
    error_code=PostgresErrorCode.RESTRICT_VIOLATION,
    exception=DeleteConstraintException(
        table_name="genres",
        referencing_table="movies"
    )
)

genres_error_handler = TableErrorHandler(
    uq_genres_name,
    uq_genres_slug,
    fk_movie_genre_associations_genre_id_genres
)