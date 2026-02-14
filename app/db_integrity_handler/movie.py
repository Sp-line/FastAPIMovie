from constants.db import PostgresErrorCode
from db_integrity_handler.base import TableErrorHandler
from exceptions.db import UniqueFieldException
from schemas.db import ConstraintRule

uq_movies_slug = ConstraintRule(
    name="uq_movies_slug",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="slug",
        table_name="movies"
    )
)

movies_error_handler = TableErrorHandler(
    uq_movies_slug
)
