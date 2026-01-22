from repositories.m2m import MovieCountryRepository, MovieGenreRepository, MoviePersonRepository
from repositories.unit_of_work import UnitOfWork
from schemas.movie_country import MovieCountryRead, MovieCountryCreate, MovieCountryUpdate, MovieCountryCompositeId
from schemas.movie_genre import MovieGenreRead, MovieGenreCreate, MovieGenreUpdate, MovieGenreCompositeId
from schemas.movie_person import MoviePersonRead, MoviePersonCreate, MoviePersonUpdate, MoviePersonCompositeId
from services.base import M2MServiceBase


class MovieCountryService(
    M2MServiceBase
    [
        MovieCountryRepository,
        MovieCountryRead,
        MovieCountryCreate,
        MovieCountryUpdate,
        MovieCountryCompositeId
    ]
):
    def __init__(
            self,
            repository: MovieCountryRepository,
            unit_of_work: UnitOfWork,
    ) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="movie_country_associations",
            read_schema_type=MovieCountryRead,
        )


class MovieGenreService(
    M2MServiceBase
    [
        MovieGenreRepository,
        MovieGenreRead,
        MovieGenreCreate,
        MovieGenreUpdate,
        MovieGenreCompositeId
    ]
):
    def __init__(
            self,
            repository: MovieGenreRepository,
            unit_of_work: UnitOfWork,
    ) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="movie_genre_associations",
            read_schema_type=MovieGenreRead,
        )


class MoviePersonService(
    M2MServiceBase
    [
        MoviePersonRepository,
        MoviePersonRead,
        MoviePersonCreate,
        MoviePersonUpdate,
        MoviePersonCompositeId
    ]
):
    def __init__(
            self,
            repository: MoviePersonRepository,
            unit_of_work: UnitOfWork,
    ) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="movie_person_associations",
            read_schema_type=MoviePersonRead,
        )
