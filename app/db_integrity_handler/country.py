from constants.db import PostgresErrorCode
from db_integrity_handler.base import TableErrorHandler
from exceptions.db import UniqueFieldException, DeleteConstraintException
from schemas.db import ConstraintRule

uq_countries_name = ConstraintRule(
    name="uq_countries_name",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="name",
        table_name="countries"
    )
)

uq_countries_slug = ConstraintRule(
    name="uq_countries_slug",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="slug",
        table_name="countries"
    )
)

fk_movie_country_associations_country_id_countries = ConstraintRule(
    name="fk_movie_country_associations_country_id_countries",
    error_code=PostgresErrorCode.RESTRICT_VIOLATION,
    exception=DeleteConstraintException(
        table_name="countries",
        referencing_table="movies"
    )
)

countries_error_handler = TableErrorHandler(
    uq_countries_name,
    uq_countries_slug,
    fk_movie_country_associations_country_id_countries
)
