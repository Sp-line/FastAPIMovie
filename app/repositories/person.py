from sqlalchemy.exc import IntegrityError

from core.models import Person
from exceptions.db import UniqueFieldException, DeleteConstraintException
from repositories.signals import SignalRepositoryBase
from schemas.base import Id
from schemas.person import PersonCreateDB, PersonUpdateDB, PersonCreateEvent, PersonUpdateEvent, person_event_schemas
from signals.base import Eventer
from signals.event_session import EventSession
from signals.person import person_base_publishers


class PersonRepository(
    SignalRepositoryBase[
        Person,
        PersonCreateDB,
        PersonUpdateDB,
        PersonCreateEvent,
        PersonUpdateEvent,
        Id
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            Person,
            session,
            Eventer(publishers=person_base_publishers),
            person_event_schemas
        )

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        err_data = self._get_integrity_error_data(exc)

        match err_data.sqlstate:
            case "23505":
                match err_data.constraint_name:
                    case "uq_persons_slug":
                        raise UniqueFieldException(field_name="slug", table_name=err_data.table_name)
            case "23001":
                match err_data.constraint_name:
                    case "fk_movie_person_associations_person_id_persons":
                        raise DeleteConstraintException(
                            table_name=err_data.table_name,
                            referencing_table="movies"
                        )
