from slugify import slugify

from repositories.person import PersonRepository
from repositories.unit_of_work import UnitOfWork
from schemas.person import PersonRead, PersonCreateDB, PersonUpdateDB, PersonCreateReq, PersonUpdateReq
from services.base import ServiceBase


class PersonService(ServiceBase[PersonRepository, PersonRead, PersonCreateReq, PersonUpdateReq]):
    def __init__(
            self,
            repository: PersonRepository,
            unit_of_work: UnitOfWork,
    ) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="persons",
            read_schema_type=PersonRead,
        )

    def _prepare_update_data(self, data: PersonUpdateReq) -> PersonUpdateDB:
        return PersonUpdateDB(**data.model_dump(exclude_unset=True))

    def _prepare_create_data(self, data: PersonCreateReq) -> PersonCreateDB:
        return PersonCreateDB(
            **data.model_dump(),
            slug=slugify(data.full_name)
        )
