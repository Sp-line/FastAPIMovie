from slugify import slugify

from exceptions.db import ObjectNotFoundException
from repositories.movie import MovieRepository
from repositories.unit_of_work import UnitOfWork
from schemas.movie import MovieRead, MovieList, MovieCreateReq, MovieCreateDB, MovieUpdateDB, MovieUpdateReq, \
    MovieDetail
from services.abc import ServiceABC
from services.file import FileService
from services.s3 import S3Service
from storage.path_builder import SlugFilePathBuilder
from storage.url_resolver import FileUrlResolver


class MovieService(
    ServiceABC[
        MovieRepository,
        MovieRead,
        MovieCreateReq,
        MovieUpdateReq,
        MovieCreateDB,
        MovieUpdateDB
    ]
):
    def __init__(
            self,
            repository: MovieRepository,
            unit_of_work: UnitOfWork,
    ) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="movies",
            read_schema_type=MovieRead
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

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[MovieList]:
        items = await self._repository.get_for_list(skip, limit)
        return [MovieList.model_validate(movie) for movie in items]

    async def get_by_id(self, movie_id: int) -> MovieDetail:
        if not (movie := await self._repository.get_for_read(movie_id)):
            raise ObjectNotFoundException(movie_id, self._table_name)
        return MovieDetail.model_validate(movie)


class MovieFileService(FileService[MovieRead, MovieUpdateDB]):
    def __init__(
            self,
            s3_service: S3Service,
            repository: MovieRepository,
            unit_of_work: UnitOfWork
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
