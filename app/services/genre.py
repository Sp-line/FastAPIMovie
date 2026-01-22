from slugify import slugify

from repositories.genre import GenreRepository
from repositories.unit_of_work import UnitOfWork
from schemas.genre import GenreRead, GenreCreateDB, GenreUpdateDB, GenreCreateReq, GenreUpdateReq
from services.base import ServiceBase


class GenreService(ServiceBase[GenreRepository, GenreRead, GenreCreateReq, GenreUpdateReq]):
    def __init__(
            self,
            repository: GenreRepository,
            unit_of_work: UnitOfWork,
    ) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="genres",
            read_schema_type=GenreRead,
        )

    def _prepare_create_data(self, data: GenreCreateReq) -> GenreCreateDB:
        return GenreCreateDB(
            **data.model_dump(),
            slug=slugify(data.name)
        )

    def _prepare_update_data(self, data: GenreUpdateReq) -> GenreUpdateDB:
        return GenreUpdateDB(**data.model_dump(exclude_unset=True))
