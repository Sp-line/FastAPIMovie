from slugify import slugify

from repositories.country import CountryRepository
from repositories.unit_of_work import UnitOfWork
from schemas.country import CountryRead, CountryUpdateDB, CountryCreateDB, CountryUpdateReq, CountryCreateReq
from services.base import ServiceBase


class CountryService(ServiceBase[CountryRepository, CountryRead, CountryCreateReq, CountryUpdateReq]):
    def __init__(
            self,
            repository: CountryRepository,
            unit_of_work: UnitOfWork,
    ) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="countries",
            read_schema_type=CountryRead,
        )

    def _prepare_create_data(self, data: CountryCreateReq) -> CountryCreateDB:
        return CountryCreateDB(
            **data.model_dump(),
            slug=slugify(data.name)
        )

    def _prepare_update_data(self, data: CountryUpdateReq) -> CountryUpdateDB:
        return CountryUpdateDB(**data.model_dump(exclude_unset=True))
