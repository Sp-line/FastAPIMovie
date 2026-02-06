from typing import Annotated, TypeAlias

from fastapi import Depends

from dependencies.cache import RedisDep
from dependencies.db import SignalUnitOfWorkDep
from dependencies.elastic import AsyncElasticDep
from dependencies.repositories import MovieRepositoryDep, \
    MovieCountryRepositoryDep, \
    MovieGenreRepositoryDep, \
    MoviePersonRepositoryDep, PersonRepositoryDep, MovieShotRepositoryDep, CountryRepositoryDep, GenreRepositoryDep
from dependencies.s3 import S3ServiceDep
from services.country import CountryService, CountrySearchService
from services.genre import GenreService, GenreSearchService
from services.m2m import MovieCountryService, MovieGenreService, MoviePersonService
from services.movie import MovieService, MovieFileService, MovieSearchService
from services.movie_shot import MovieShotService, MovieShotFileService
from services.person import PersonService, PersonFileService, PersonSearchService


def get_movie_service(
        repository: MovieRepositoryDep,
        uow: SignalUnitOfWorkDep,
        cache: RedisDep
) -> MovieService:
    return MovieService(repository, uow, cache)


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
        cache: RedisDep
) -> MoviePersonService:
    return MoviePersonService(repository, uow, cache)


def get_movie_file_service(
        repository: MovieRepositoryDep,
        uow: SignalUnitOfWorkDep,
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
        uow: SignalUnitOfWorkDep,
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
        uow: SignalUnitOfWorkDep,
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


def get_country_search_service(elasticsearch: AsyncElasticDep) -> CountrySearchService:
    return CountrySearchService(elasticsearch)


def get_person_search_service(elasticsearch: AsyncElasticDep) -> PersonSearchService:
    return PersonSearchService(elasticsearch)


def get_genre_search_service(elasticsearch: AsyncElasticDep) -> GenreSearchService:
    return GenreSearchService(elasticsearch)


def get_movie_search_service(elasticsearch: AsyncElasticDep) -> MovieSearchService:
    return MovieSearchService(elasticsearch)


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

CountrySearchServiceDep: TypeAlias = Annotated[CountrySearchService, Depends(get_country_search_service)]
PersonSearchServiceDep: TypeAlias = Annotated[PersonSearchService, Depends(get_person_search_service)]
GenreSearchServiceDep: TypeAlias = Annotated[GenreSearchService, Depends(get_genre_search_service)]
MovieSearchServiceDep: TypeAlias = Annotated[MovieSearchService, Depends(get_movie_search_service)]
