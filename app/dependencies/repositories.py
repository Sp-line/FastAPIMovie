from typing import TypeAlias, Annotated

from fastapi import Depends

from dependencies.db import EventSessionDep
from repositories.country import CountryRepository
from repositories.genre import GenreRepository
from repositories.m2m import MovieCountryRepository, MovieGenreRepository, MoviePersonRepository
from repositories.movie import MovieRepository
from repositories.movie_shot import MovieShotRepository
from repositories.person import PersonRepository


def get_movie_repository(session: EventSessionDep) -> MovieRepository:
    return MovieRepository(session)


def get_person_repository(session: EventSessionDep) -> PersonRepository:
    return PersonRepository(session)


def get_movie_shot_repository(session: EventSessionDep) -> MovieShotRepository:
    return MovieShotRepository(session)


def get_genre_repository(session: EventSessionDep) -> GenreRepository:
    return GenreRepository(session)


def get_country_repository(session: EventSessionDep) -> CountryRepository:
    return CountryRepository(session)


def get_movie_country_repository(session: EventSessionDep) -> MovieCountryRepository:
    return MovieCountryRepository(session)


def get_movie_genre_repository(session: EventSessionDep) -> MovieGenreRepository:
    return MovieGenreRepository(session)


def get_movie_person_repository(session: EventSessionDep) -> MoviePersonRepository:
    return MoviePersonRepository(session)


MovieRepositoryDep: TypeAlias = Annotated[MovieRepository, Depends(get_movie_repository)]
MovieCountryRepositoryDep: TypeAlias = Annotated[MovieCountryRepository, Depends(get_movie_country_repository)]
MovieGenreRepositoryDep: TypeAlias = Annotated[MovieGenreRepository, Depends(get_movie_genre_repository)]
MoviePersonRepositoryDep: TypeAlias = Annotated[MoviePersonRepository, Depends(get_movie_person_repository)]
PersonRepositoryDep: TypeAlias = Annotated[PersonRepository, Depends(get_person_repository)]
MovieShotRepositoryDep: TypeAlias = Annotated[MovieShotRepository, Depends(get_movie_shot_repository)]
CountryRepositoryDep: TypeAlias = Annotated[CountryRepository, Depends(get_country_repository)]
GenreRepositoryDep: TypeAlias = Annotated[GenreRepository, Depends(get_genre_repository)]
