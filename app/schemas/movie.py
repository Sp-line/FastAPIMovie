from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import MOVIE_TITLE_MAX_LEN, MOVIE_SLUG_MAX_LEN, MOVIE_DURATION_MIN_VALUE, MOVIE_DURATION_MAX_VALUE, \
    MOVIE_AGE_RATING_MAX_LEN, IMAGE_URL_MAX_LEN
from constants.base import IMAGE_URL_MIN_LEN
from constants.movie import MOVIE_RELEASE_YEAR_MIN_VALUE, MOVIE_TITLE_MIN_LEN, MOVIE_SLUG_MIN_LEN, \
    MOVIE_AGE_RATING_MIN_LEN
from schemas.country import CountryRead
from schemas.genre import GenreRead
from schemas.movie_person import MoviePersonRelatedRead
from schemas.movie_shot import MovieRelatedShotRead


class MovieSummaryBase(BaseModel):
    title: Annotated[str, Field(min_length=MOVIE_TITLE_MIN_LEN, max_length=MOVIE_TITLE_MAX_LEN)]
    slug: Annotated[str, Field(min_length=MOVIE_SLUG_MIN_LEN, max_length=MOVIE_SLUG_MAX_LEN)]
    duration: Annotated[int, Field(ge=MOVIE_DURATION_MIN_VALUE, le=MOVIE_DURATION_MAX_VALUE)]
    release_year: Annotated[int, Field(ge=MOVIE_RELEASE_YEAR_MIN_VALUE)]
    poster_url: Annotated[str | None, Field(min_length=IMAGE_URL_MIN_LEN, max_length=IMAGE_URL_MAX_LEN)] = None
    age_rating: Annotated[
        str | None, Field(min_length=MOVIE_AGE_RATING_MIN_LEN, max_length=MOVIE_AGE_RATING_MAX_LEN)] = None


class MovieBase(MovieSummaryBase):
    description: str | None = None
    premiere_date: datetime | None = None


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: Annotated[str | None, Field(min_length=MOVIE_TITLE_MIN_LEN, max_length=MOVIE_TITLE_MAX_LEN)] = None
    slug: Annotated[str | None, Field(min_length=MOVIE_SLUG_MIN_LEN, max_length=MOVIE_SLUG_MAX_LEN)] = None
    description: str | None = None
    duration: Annotated[int | None, Field(ge=MOVIE_DURATION_MIN_VALUE, le=MOVIE_DURATION_MAX_VALUE)] = None
    age_rating: Annotated[
        str | None, Field(min_length=MOVIE_AGE_RATING_MIN_LEN, max_length=MOVIE_AGE_RATING_MAX_LEN)] = None
    premiere_date: datetime | None = None
    release_year: Annotated[int | None, Field(ge=MOVIE_RELEASE_YEAR_MIN_VALUE)] = None
    poster_url: Annotated[str | None, Field(min_length=IMAGE_URL_MIN_LEN, max_length=IMAGE_URL_MAX_LEN)] = None


class MovieRead(MovieBase):
    id: int

    genres: Annotated[list[GenreRead], Field(default_factory=list)]
    countries: Annotated[list[CountryRead], Field(default_factory=list)]
    shots: Annotated[list[MovieRelatedShotRead], Field(default_factory=list)]
    person_associations: Annotated[list[MoviePersonRelatedRead], Field(default_factory=list)]

    model_config = ConfigDict(from_attributes=True)


class MovieList(MovieSummaryBase):
    id: int

    genres: Annotated[list[GenreRead], Field(default_factory=list)]

    model_config = ConfigDict(from_attributes=True)
