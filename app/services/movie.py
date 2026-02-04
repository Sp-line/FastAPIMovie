import orjson
from redis.asyncio.client import Redis as AsyncRedis
from slugify import slugify

from exceptions.db import ObjectNotFoundException
from repositories.movie import MovieRepository
from repositories.signals import SignalUnitOfWork
from schemas.movie import MovieRead, MovieList, MovieCreateReq, MovieCreateDB, MovieUpdateDB, MovieUpdateReq, \
    MovieDetail, MovieCacheConfig
from services.cache import CacheServiceABC
from services.file import FileService
from services.s3 import S3Service
from storage.path_builder import SlugFilePathBuilder
from storage.url_resolver import FileUrlResolver


class MovieService(
    CacheServiceABC[
        MovieRepository,
        MovieRead,
        MovieCreateReq,
        MovieUpdateReq,
        MovieCreateDB,
        MovieUpdateDB,
        MovieCacheConfig
    ]
):
    def __init__(
            self,
            repository: MovieRepository,
            unit_of_work: SignalUnitOfWork,
            cache: AsyncRedis
    ) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="movies",
            read_schema_type=MovieRead,
            cache=cache,
            cache_model_config=MovieCacheConfig()
        )

    @staticmethod
    def _prepare_update_data(data: MovieUpdateReq) -> MovieUpdateDB:
        return MovieUpdateDB(**data.model_dump(exclude_unset=True))

    @staticmethod
    def _prepare_create_data(data: MovieCreateReq) -> MovieCreateDB:
        return MovieCreateDB(
            **data.model_dump(),
            slug=slugify(data.title)
        )

    async def get_for_list(self, skip: int = 0, limit: int = 100) -> list[MovieList]:
        key = self._cache_model_config.list_summary_key.format(
            table_name=self._table_name,
            skip=skip,
            limit=limit
        )

        if (cached := await self._cache.get(key)) is not None:
            return [MovieList.model_validate(obj) for obj in orjson.loads(cached)]

        objs = [MovieList.model_validate(obj) for obj in await self._repository.get_for_list(skip, limit)]

        data_to_cache = orjson.dumps(
            [obj.model_dump() for obj in objs]
        )

        await self._cache.set(
            key,
            data_to_cache,
            self._cache_model_config.list_summary_ttl
        )

        return objs

    async def get_for_detail(self, obj_id: int) -> MovieDetail:
        key = self._cache_model_config.detail_key.format(
            table_name=self._table_name,
            obj_id=obj_id
        )

        if (cached := await self._cache.get(key)) is not None:
            return MovieDetail.model_validate(orjson.loads(cached))

        if db_obj := await self._repository.get_for_detail(obj_id):
            obj = MovieDetail.model_validate(db_obj)
        else:
            raise ObjectNotFoundException(
                obj_id=obj_id,
                table_name=self._table_name
            )

        data_to_cache = orjson.dumps(obj.model_dump())

        await self._cache.set(
            key,
            data_to_cache,
            self._cache_model_config.detail_ttl
        )

        return obj


class MovieFileService(FileService[MovieRead, MovieUpdateDB]):
    def __init__(
            self,
            s3_service: S3Service,
            repository: MovieRepository,
            unit_of_work: SignalUnitOfWork
    ):
        super().__init__(
            s3_service=s3_service,
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="movies",
            url_field="poster_url",
            read_schema_type=MovieRead,
            update_schema_type=MovieUpdateDB,
            url_resolver=FileUrlResolver(),
            path_builder=SlugFilePathBuilder[MovieRead](folder="movies/posters", field="slug"),
        )
