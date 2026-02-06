from elasticsearch import AsyncElasticsearch
from redis.asyncio.client import Redis as AsyncRedis
from slugify import slugify

from repositories.country import CountryRepository
from repositories.signals import SignalUnitOfWork
from schemas.cache import ModelCacheConfig
from schemas.country import CountryRead, CountryUpdateDB, CountryCreateDB, CountryUpdateReq, CountryCreateReq, \
    CountrySearchRead
from services.cache import CacheServiceABC
from services.search import SearchServiceBase


class CountryService(
    CacheServiceABC[
        CountryRepository,
        CountryRead,
        CountryCreateReq,
        CountryUpdateReq,
        CountryCreateDB,
        CountryUpdateDB,
        ModelCacheConfig
    ]
):
    def __init__(
            self,
            repository: CountryRepository,
            unit_of_work: SignalUnitOfWork,
            cache: AsyncRedis,
    ) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="countries",
            read_schema_type=CountryRead,
            cache=cache,
            cache_model_config=ModelCacheConfig()
        )

    @staticmethod
    def _prepare_create_data(data: CountryCreateReq) -> CountryCreateDB:
        return CountryCreateDB(
            **data.model_dump(),
            slug=slugify(data.name)
        )

    @staticmethod
    def _prepare_update_data(data: CountryUpdateReq) -> CountryUpdateDB:
        return CountryUpdateDB(**data.model_dump(exclude_unset=True))


class CountrySearchService(SearchServiceBase[CountrySearchRead]):
    def __init__(self, client: AsyncElasticsearch) -> None:
        super().__init__(
            client,
            CountrySearchRead,
            "countries",
            ["name", ]
        )
