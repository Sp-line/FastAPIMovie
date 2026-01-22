from asyncpg import exceptions as pg_exc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Country
from exceptions.db import UniqueFieldException, DeleteConstraintException
from repositories.base import RepositoryBase
from schemas.country import CountryCreateDB, CountryUpdateDB


class CountryRepository(RepositoryBase[Country, CountryCreateDB, CountryUpdateDB]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Country, session)

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        orig = exc.orig

        if isinstance(orig, pg_exc.UniqueViolationError):
            match getattr(exc.orig, "constraint_name", None):
                case "uq_countries_name":
                    raise UniqueFieldException(field_name="name", table_name="countries")
                case "uq_countries_slug":
                    raise UniqueFieldException(field_name="slug", table_name="countries")
        elif isinstance(orig, pg_exc.ForeignKeyViolationError):
            match getattr(orig, "constraint_name", None):
                case "fk_movie_country_associations_country_id_countries":
                    raise DeleteConstraintException(
                        table_name="countries",
                        referencing_table="movies"
                    )