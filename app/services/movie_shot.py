from repositories.movie_shot import MovieShotRepository
from repositories.unit_of_work import UnitOfWork
from schemas.movie_shot import MovieShotRead, MovieShotCreateReq, MovieShotCreateDB, MovieShotUpdateDB, \
    MovieShotUpdateReq
from services.base import IntServiceABC
from services.file import FileService
from services.s3 import S3Service
from storage.path_builder import SlugFilePathBuilder
from storage.url_resolver import FileUrlResolver


class MovieShotService(
    IntServiceABC[
        MovieShotRepository,
        MovieShotRead,
        MovieShotCreateReq,
        MovieShotUpdateReq,
        MovieShotCreateDB,
        MovieShotUpdateDB
    ]
):
    def __init__(
            self,
            repository: MovieShotRepository,
            unit_of_work: UnitOfWork,
    ) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="movie_shots",
            read_schema_type=MovieShotRead,
        )

    @staticmethod
    def _prepare_update_data(data: MovieShotUpdateReq) -> MovieShotUpdateDB:
        return MovieShotUpdateDB(**data.model_dump(exclude_unset=True))

    @staticmethod
    def _prepare_create_data(data: MovieShotCreateReq) -> MovieShotCreateDB:
        return MovieShotCreateDB(**data.model_dump())


class MovieShotFileService(FileService[MovieShotRead, MovieShotUpdateDB]):
    def __init__(
            self,
            s3_service: S3Service,
            repository: MovieShotRepository,
            unit_of_work: UnitOfWork
    ):
        super().__init__(
            s3_service=s3_service,
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="movie_shots",
            url_field="image_url",
            read_schema_type=MovieShotRead,
            update_schema_type=MovieShotUpdateDB,
            url_resolver=FileUrlResolver(),
            path_builder=SlugFilePathBuilder[MovieShotRead](folder="movie_shots/images", field="slug")
        )
