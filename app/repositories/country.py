from sqlalchemy.exc import IntegrityError

from core.models import Country
from exceptions.db import UniqueFieldException, DeleteConstraintException
from repositories.signals import SignalRepositoryBase
from schemas.base import Id
from schemas.country import CountryCreateDB, CountryUpdateDB, CountryCreateEvent, CountryUpdateEvent, \
    country_event_schemas
from signals.base import Eventer
from signals.country import country_base_publishers
from signals.event_session import EventSession


class CountryRepository(
    SignalRepositoryBase[
        Country,
        CountryCreateDB,
        CountryUpdateDB,
        CountryCreateEvent,
        CountryUpdateEvent,
        Id
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            Country,
            session,
            Eventer(publishers=country_base_publishers),
            country_event_schemas
        )

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
