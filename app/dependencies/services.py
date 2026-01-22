from typing import Annotated

from fastapi import Depends

from dependencies.db import get_uow
from dependencies.repositories import get_movie_repository, get_person_repository, get_movie_shot_repository, \
    get_country_repository, get_genre_repository, get_movie_country_repository, get_movie_genre_repository, \
    get_movie_person_repository
from dependencies.s3 import get_s3_service
from repositories.country import CountryRepository
from repositories.genre import GenreRepository
from repositories.m2m import MovieCountryRepository, MovieGenreRepository, MoviePersonRepository
from repositories.movie import MovieRepository
from repositories.movie_shot import MovieShotRepository
from repositories.person import PersonRepository
from repositories.unit_of_work import UnitOfWork
from services.country import CountryService
from services.genre import GenreService
from services.m2m import MovieCountryService, MovieGenreService, MoviePersonService
from services.movie import MovieService, MovieFileService
from services.movie_shot import MovieShotService, MovieShotFileService
from services.person import PersonService, PersonFileService
from services.s3 import S3Service


def get_movie_service(
        repository: Annotated[MovieRepository, Depends(get_movie_repository)],
        uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> MovieService:
    return MovieService(repository, uow)


def get_movie_country_service(
        repository: Annotated[MovieCountryRepository, Depends(get_movie_country_repository)],
        uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> MovieCountryService:
    return MovieCountryService(repository, uow)


def get_movie_genre_service(
        repository: Annotated[MovieGenreRepository, Depends(get_movie_genre_repository)],
        uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> MovieGenreService:
    return MovieGenreService(repository, uow)


def get_movie_person_service(
        repository: Annotated[MoviePersonRepository, Depends(get_movie_person_repository)],
        uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> MoviePersonService:
    return MoviePersonService(repository, uow)


def get_movie_file_service(
        repository: Annotated[MovieRepository, Depends(get_movie_repository)],
        uow: Annotated[UnitOfWork, Depends(get_uow)],
        s3: Annotated[S3Service, Depends(get_s3_service)],
) -> MovieFileService:
    return MovieFileService(s3, repository, uow)


def get_person_service(
        repository: Annotated[PersonRepository, Depends(get_person_repository)],
        uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> PersonService:
    return PersonService(repository, uow)


def get_person_file_service(
        repository: Annotated[PersonRepository, Depends(get_person_repository)],
        uow: Annotated[UnitOfWork, Depends(get_uow)],
        s3: Annotated[S3Service, Depends(get_s3_service)],
) -> PersonFileService:
    return PersonFileService(s3, repository, uow)


def get_movie_shot_service(
        repository: Annotated[MovieShotRepository, Depends(get_movie_shot_repository)],
        uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> MovieShotService:
    return MovieShotService(repository, uow)


def get_movie_shot_file_service(
        repository: Annotated[MovieShotRepository, Depends(get_movie_shot_repository)],
        uow: Annotated[UnitOfWork, Depends(get_uow)],
        s3: Annotated[S3Service, Depends(get_s3_service)],
) -> MovieShotFileService:
    return MovieShotFileService(s3, repository, uow)


def get_country_service(
        repository: Annotated[CountryRepository, Depends(get_country_repository)],
        uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> CountryService:
    return CountryService(repository, uow)


def get_genre_service(
        repository: Annotated[GenreRepository, Depends(get_genre_repository)],
        uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> GenreService:
    return GenreService(repository, uow)


MovieServiceDep = Annotated[MovieService, Depends(get_movie_service)]
MovieFileServiceDep = Annotated[MovieFileService, Depends(get_movie_file_service)]

MovieShotServiceDep = Annotated[MovieShotService, Depends(get_movie_shot_service)]
MovieShotFileServiceDep = Annotated[MovieShotFileService, Depends(get_movie_shot_file_service)]

MovieCountryServiceDep = Annotated[MovieCountryService, Depends(get_movie_country_service)]
MovieGenreServiceDep = Annotated[MovieGenreService, Depends(get_movie_genre_service)]
MoviePersonServiceDep = Annotated[MoviePersonService, Depends(get_movie_person_service)]

PersonServiceDep = Annotated[PersonService, Depends(get_person_service)]
PersonFileServiceDep = Annotated[PersonFileService, Depends(get_person_file_service)]
CountryServiceDep = Annotated[CountryService, Depends(get_country_service)]
GenreServiceDep = Annotated[GenreService, Depends(get_genre_service)]
