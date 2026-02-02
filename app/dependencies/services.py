from typing import Annotated, TypeAlias

from fastapi import Depends

from dependencies.cache import RedisDep
from dependencies.db import UnitOfWorkDep, SignalUnitOfWorkDep
from dependencies.repositories import MovieRepositoryDep, \
    MovieCountryRepositoryDep, \
    MovieGenreRepositoryDep, \
    MoviePersonRepositoryDep, PersonRepositoryDep, MovieShotRepositoryDep, CountryRepositoryDep, GenreRepositoryDep
from dependencies.s3 import S3ServiceDep
from services.country import CountryService
from services.genre import GenreService
from services.m2m import MovieCountryService, MovieGenreService, MoviePersonService
from services.movie import MovieService, MovieFileService
from services.movie_shot import MovieShotService, MovieShotFileService
from services.person import PersonService, PersonFileService


def get_movie_service(
        repository: MovieRepositoryDep,
        uow: UnitOfWorkDep,
) -> MovieService:
    return MovieService(repository, uow)


def get_movie_country_service(
        repository: MovieCountryRepositoryDep,
        uow: SignalUnitOfWorkDep,
) -> MovieCountryService:
    return MovieCountryService(repository, uow)


def get_movie_genre_service(
        repository: MovieGenreRepositoryDep,
        uow: SignalUnitOfWorkDep,
) -> MovieGenreService:
    return MovieGenreService(repository, uow)


def get_movie_person_service(
        repository: MoviePersonRepositoryDep,
        uow: SignalUnitOfWorkDep,
) -> MoviePersonService:
    return MoviePersonService(repository, uow)


def get_movie_file_service(
        repository: MovieRepositoryDep,
        uow: UnitOfWorkDep,
        s3: S3ServiceDep,
) -> MovieFileService:
    return MovieFileService(s3, repository, uow)


def get_person_service(
        repository: PersonRepositoryDep,
        uow: SignalUnitOfWorkDep,
        cache: RedisDep
) -> PersonService:
    return PersonService(repository, uow, cache)


def get_person_file_service(
        repository: PersonRepositoryDep,
        uow: UnitOfWorkDep,
        s3: S3ServiceDep,
) -> PersonFileService:
    return PersonFileService(s3, repository, uow)


def get_movie_shot_service(
        repository: MovieShotRepositoryDep,
        uow: SignalUnitOfWorkDep,
) -> MovieShotService:
    return MovieShotService(repository, uow)


def get_movie_shot_file_service(
        repository: MovieShotRepositoryDep,
        uow: UnitOfWorkDep,
        s3: S3ServiceDep,
) -> MovieShotFileService:
    return MovieShotFileService(s3, repository, uow)


def get_country_service(
        repository: CountryRepositoryDep,
        uow: SignalUnitOfWorkDep,
        cache: RedisDep
) -> CountryService:
    return CountryService(repository, uow, cache)


def get_genre_service(
        repository: GenreRepositoryDep,
        uow: SignalUnitOfWorkDep,
        cache: RedisDep,
) -> GenreService:
    return GenreService(repository, uow, cache)


MovieServiceDep: TypeAlias = Annotated[MovieService, Depends(get_movie_service)]
MovieFileServiceDep: TypeAlias = Annotated[MovieFileService, Depends(get_movie_file_service)]

MovieShotServiceDep: TypeAlias = Annotated[MovieShotService, Depends(get_movie_shot_service)]
MovieShotFileServiceDep: TypeAlias = Annotated[MovieShotFileService, Depends(get_movie_shot_file_service)]

MovieCountryServiceDep: TypeAlias = Annotated[MovieCountryService, Depends(get_movie_country_service)]
MovieGenreServiceDep: TypeAlias = Annotated[MovieGenreService, Depends(get_movie_genre_service)]
MoviePersonServiceDep: TypeAlias = Annotated[MoviePersonService, Depends(get_movie_person_service)]

PersonServiceDep: TypeAlias = Annotated[PersonService, Depends(get_person_service)]
PersonFileServiceDep: TypeAlias = Annotated[PersonFileService, Depends(get_person_file_service)]
CountryServiceDep: TypeAlias = Annotated[CountryService, Depends(get_country_service)]
GenreServiceDep: TypeAlias = Annotated[GenreService, Depends(get_genre_service)]
