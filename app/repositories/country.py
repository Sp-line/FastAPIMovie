from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Country
from exceptions.db import UniqueFieldException, DeleteConstraintException
from repositories.base import RepositoryBase
from schemas.country import CountryCreateDB, CountryUpdateDB


class CountryRepository(IntRepositoryBase[Country, CountryCreateDB, CountryUpdateDB]):
    def __init__(self, session: AsyncSession) -> None:
class CountryRepository(RepositoryBase[Country, CountryCreateDB, CountryUpdateDB]):
        super().__init__(Country, session)

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        err_data = self._get_integrity_error_data(exc)

        match err_data.sqlstate:
            case "23505":
                match err_data.constraint_name:
                    case "uq_countries_name":
                        raise UniqueFieldException(field_name="name", table_name=err_data.table_name)
                    case "uq_countries_slug":
                        raise UniqueFieldException(field_name="slug", table_name=err_data.table_name)
            case "23001":
                match err_data.constraint_name:
                    case "fk_movie_country_associations_country_id_countries":
                        raise DeleteConstraintException(
                            table_name=err_data.table_name,
                            referencing_table="movies"
                        )
