from sqlalchemy.exc import IntegrityError

from core.models import Person
from exceptions.db import UniqueFieldException, DeleteConstraintException
from repositories.base import RepositoryBase
from schemas.person import PersonCreateDB, PersonUpdateDB
from signals.event_session import EventSession


class PersonRepository(RepositoryBase[Person, PersonCreateDB, PersonUpdateDB]):
    def __init__(self, session: EventSession) -> None:
        super().__init__(Person, session)

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
