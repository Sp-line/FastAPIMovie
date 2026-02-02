from redis.asyncio.client import Redis as AsyncRedis
from slugify import slugify

from repositories.genre import GenreRepository
from repositories.unit_of_work import UnitOfWork
from schemas.cache import ModelCacheConfig
from schemas.genre import GenreRead, GenreCreateDB, GenreUpdateDB, GenreCreateReq, GenreUpdateReq
from services.cache import CacheServiceABC


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
            unit_of_work: UnitOfWork,
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
