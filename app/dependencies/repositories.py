from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper as db
from repositories.country import CountryRepository
from repositories.genre import GenreRepository
from repositories.m2m import MovieCountryRepository, MovieGenreRepository, MoviePersonRepository
from repositories.movie import MovieRepository
from repositories.movie_shot import MovieShotRepository
from repositories.person import PersonRepository


def get_movie_repository(session: Annotated[AsyncSession, Depends(db.session_getter)]) -> MovieRepository:
    return MovieRepository(session)


def get_person_repository(session: Annotated[AsyncSession, Depends(db.session_getter)]) -> PersonRepository:
    return PersonRepository(session)


def get_movie_shot_repository(session: Annotated[AsyncSession, Depends(db.session_getter)]) -> MovieShotRepository:
    return MovieShotRepository(session)


def get_genre_repository(session: Annotated[AsyncSession, Depends(db.session_getter)]) -> GenreRepository:
    return GenreRepository(session)


def get_country_repository(session: Annotated[AsyncSession, Depends(db.session_getter)]) -> CountryRepository:
    return CountryRepository(session)


def get_movie_country_repository(session: Annotated[AsyncSession, Depends(db.session_getter)]) -> MovieCountryRepository:
    return MovieCountryRepository(session)


def get_movie_genre_repository(session: Annotated[AsyncSession, Depends(db.session_getter)]) -> MovieGenreRepository:
    return MovieGenreRepository(session)


def get_movie_person_repository(session: Annotated[AsyncSession, Depends(db.session_getter)]) -> MoviePersonRepository:
    return MoviePersonRepository(session)
