from slugify import slugify

from core.models import Person
from repositories.person import PersonRepository
from repositories.unit_of_work import UnitOfWork
from schemas.person import PersonRead, PersonCreateDB, PersonUpdateDB, PersonCreateReq, PersonUpdateReq
from services.base import IntServiceBase
from services.file import FileService
from services.s3 import S3Service
from storage.path_builder import SlugFilePathBuilder
from storage.url_resolver import FileUrlResolver


class PersonService(IntServiceBase[PersonRepository, PersonRead, PersonCreateReq, PersonUpdateReq]):
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

    @staticmethod
    def _prepare_update_data(data: PersonUpdateReq) -> PersonUpdateDB:
        return PersonUpdateDB(**data.model_dump(exclude_unset=True))

    @staticmethod
    def _prepare_create_data(data: PersonCreateReq) -> PersonCreateDB:
        return PersonCreateDB(
            **data.model_dump(),
            slug=slugify(data.full_name)
        )


class PersonFileService(FileService[PersonRead]):
    def __init__(
            self,
            s3_service: S3Service,
            repository: PersonRepository,
            unit_of_work: UnitOfWork
    ):
        super().__init__(
            s3_service=s3_service,
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="persons",
            url_field="photo_url",
            read_schema_type=PersonRead,
            update_schema_type=PersonUpdateDB,
            url_resolver=FileUrlResolver(),
            path_builder=SlugFilePathBuilder[Person](folder="persons/photos", field="slug"),
        )
