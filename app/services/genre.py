from elasticsearch import AsyncElasticsearch
from redis.asyncio.client import Redis as AsyncRedis
from slugify import slugify

from repositories.genre import GenreRepository
from repositories.signals import SignalUnitOfWork
from schemas.cache import ModelCacheConfig
from schemas.genre import GenreRead, GenreCreateDB, GenreUpdateDB, GenreCreateReq, GenreUpdateReq, GenreSearchRead
from services.cache import CacheServiceABC
from services.search import SearchServiceBase


class GenreService(
    CacheServiceABC[
        GenreRepository,
        GenreRead,
        GenreCreateReq,
        GenreUpdateReq,
        GenreCreateDB,
        GenreUpdateDB,
        ModelCacheConfig
    ]
):
    def __init__(
            self,
            repository: GenreRepository,
            unit_of_work: SignalUnitOfWork,
            cache: AsyncRedis
    ) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="genres",
            read_schema_type=GenreRead,
            cache=cache,
            cache_model_config=ModelCacheConfig()
        )

    @staticmethod
    def _prepare_create_data(data: GenreCreateReq) -> GenreCreateDB:
        return GenreCreateDB(
            **data.model_dump(),
            slug=slugify(data.name)
        )

    @staticmethod
    def _prepare_update_data(data: GenreUpdateReq) -> GenreUpdateDB:
        return GenreUpdateDB(**data.model_dump(exclude_unset=True))


class GenreSearchService(SearchServiceBase[GenreSearchRead]):
    def __init__(self, client: AsyncElasticsearch) -> None:
        super().__init__(
            client,
            GenreSearchRead,
            "genres",
            ["name", ]
        )
