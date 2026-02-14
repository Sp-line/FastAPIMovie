from constants.db import PostgresErrorCode
from db_integrity_handler.base import TableErrorHandler
from exceptions.db import UniqueFieldException, DeleteConstraintException
from schemas.db import ConstraintRule

uq_persons_slug = ConstraintRule(
    name="uq_persons_slug",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="slug",
        table_name="persons"
    )
)

fk_movie_person_associations_person_id_persons = ConstraintRule(
    name="fk_movie_person_associations_person_id_persons",
    error_code=PostgresErrorCode.RESTRICT_VIOLATION,
    exception=DeleteConstraintException(
        table_name="persons",
        referencing_table="movies"
    )
)

persons_error_handler = TableErrorHandler(
    uq_persons_slug,
    fk_movie_person_associations_person_id_persons
)
