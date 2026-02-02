from repositories.m2m import MovieCountryRepository, MovieGenreRepository, MoviePersonRepository
from repositories.signals import SignalUnitOfWork
from schemas.movie_country import MovieCountryRead, MovieCountryCreate, MovieCountryUpdate
from schemas.movie_genre import MovieGenreRead, MovieGenreCreate, MovieGenreUpdate
from schemas.movie_person import MoviePersonRead, MoviePersonCreate, MoviePersonUpdate
from services.abc import ServiceABC


class MovieCountryService(
    ServiceABC
    [
        MovieCountryRepository,
        MovieCountryRead,
        MovieCountryCreate,
        MovieCountryUpdate,
        MovieCountryCreate,
        MovieCountryUpdate,
    ]
):
    def __init__(
            self,
            repository: MovieCountryRepository,
            unit_of_work: SignalUnitOfWork,
    ) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="movie_country_associations",
            read_schema_type=MovieCountryRead,
        )

    @staticmethod
    def _prepare_create_data(data: MovieCountryCreate) -> MovieCountryCreate:
        return data

    @staticmethod
    def _prepare_update_data(data: MovieCountryUpdate) -> MovieCountryUpdate:
        return data


class MovieGenreService(
    ServiceABC
    [
        MovieGenreRepository,
        MovieGenreRead,
        MovieGenreCreate,
        MovieGenreUpdate,
        MovieGenreCreate,
        MovieGenreUpdate,
    ]
):
    def __init__(
            self,
            repository: MovieGenreRepository,
            unit_of_work: SignalUnitOfWork,
    ) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="movie_genre_associations",
            read_schema_type=MovieGenreRead,
        )

    @staticmethod
    def _prepare_create_data(data: MovieGenreCreate) -> MovieGenreCreate:
        return data

    @staticmethod
    def _prepare_update_data(data: MovieGenreUpdate) -> MovieGenreUpdate:
        return data


class MoviePersonService(
    ServiceABC
    [
        MoviePersonRepository,
        MoviePersonRead,
        MoviePersonCreate,
        MoviePersonUpdate,
        MoviePersonCreate,
        MoviePersonUpdate,
    ]
):
    def __init__(
            self,
            repository: MoviePersonRepository,
            unit_of_work: SignalUnitOfWork,
    ) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="movie_person_associations",
            read_schema_type=MoviePersonRead,
        )

    @staticmethod
    def _prepare_create_data(data: MoviePersonCreate) -> MoviePersonCreate:
        return data

    @staticmethod
    def _prepare_update_data(data: MoviePersonUpdate) -> MoviePersonUpdate:
        return data
