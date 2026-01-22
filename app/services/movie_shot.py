from repositories.movie_shot import MovieShotRepository
from repositories.unit_of_work import UnitOfWork
from schemas.movie_shot import MovieShotRead, MovieShotCreateReq, MovieShotCreateDB, MovieShotUpdateDB, \
    MovieShotUpdateReq
from services.base import ServiceBase


class MovieShotService(ServiceBase[MovieShotRepository, MovieShotRead, MovieShotCreateReq, MovieShotUpdateReq]):
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

    def _prepare_update_data(self, data: MovieShotUpdateReq) -> MovieShotUpdateDB:
        return MovieShotUpdateDB(**data.model_dump(exclude_unset=True))

    def _prepare_create_data(self, data: MovieShotCreateReq) -> MovieShotCreateDB:
        return MovieShotCreateDB(**data.model_dump())
