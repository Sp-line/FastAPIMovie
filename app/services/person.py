from elasticsearch import AsyncElasticsearch
from redis.asyncio.client import Redis as AsyncRedis
from slugify import slugify

from repositories.person import PersonRepository
from repositories.signals import SignalUnitOfWork
from schemas.cache import ModelCacheConfig
from schemas.person import PersonRead, PersonCreateDB, PersonUpdateDB, PersonCreateReq, PersonUpdateReq, \
    PersonSearchRead
from services.cache import CacheServiceABC
from services.file import FileService
from services.s3 import S3Service
from services.search import SearchServiceBase
from storage.path_builder import SlugFilePathBuilder
from storage.url_resolver import FileUrlResolver


class PersonService(
    CacheServiceABC[
        PersonRepository,
        PersonRead,
        PersonCreateReq,
        PersonUpdateReq,
        PersonCreateDB,
        PersonUpdateDB,
        ModelCacheConfig
    ]
):
    def __init__(
            self,
            repository: PersonRepository,
            unit_of_work: SignalUnitOfWork,
            cache: AsyncRedis
    ) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="persons",
            read_schema_type=PersonRead,
            cache=cache,
            cache_model_config=ModelCacheConfig()
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


class PersonFileService(FileService[PersonRead, PersonUpdateDB]):
    def __init__(
            self,
            s3_service: S3Service,
            repository: PersonRepository,
            unit_of_work: SignalUnitOfWork
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
            path_builder=SlugFilePathBuilder[PersonRead](folder="persons/photos", field="slug"),
        )


class PersonSearchService(SearchServiceBase[PersonSearchRead]):
    def __init__(self, client: AsyncElasticsearch) -> None:
        super().__init__(
            client,
            PersonSearchRead,
            "persons",
            ["full_name", ]
        )
