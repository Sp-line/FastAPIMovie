from asyncpg import exceptions as pg_exc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Person
from exceptions.db import UniqueFieldException, DeleteConstraintException
from repositories.base import RepositoryBase
from schemas.person import PersonCreateDB, PersonUpdateDB


class PersonRepository(RepositoryBase[Person, PersonCreateDB, PersonUpdateDB]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Person, session)

    def _handle_integrity_error(self, exc: IntegrityError) -> None:
        orig = exc.orig

        if isinstance(orig, pg_exc.UniqueViolationError):
            match getattr(exc.orig, "constraint_name", None):
                case "uq_persons_slug":
                    raise UniqueFieldException(field_name="slug", table_name="persons")
        elif isinstance(orig, pg_exc.ForeignKeyViolationError):
            match getattr(orig, "constraint_name", None):
                case "fk_movie_person_associations_person_id_persons":
                    raise DeleteConstraintException(
                        table_name="persons",
                        referencing_table="movies"
                    )