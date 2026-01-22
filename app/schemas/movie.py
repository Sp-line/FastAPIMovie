from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import MovieLimits, ImageUrlLimits
from schemas.country import CountryRead
from schemas.genre import GenreRead
from schemas.movie_person import MoviePersonRelatedRead
from schemas.movie_shot import MovieRelatedShotRead


class MovieSummaryBase(BaseModel):
    title: Annotated[str, Field(min_length=MovieLimits.TITLE_MIN, max_length=MovieLimits.TITLE_MAX)]
    slug: Annotated[str, Field(min_length=MovieLimits.SLUG_MIN, max_length=MovieLimits.SLUG_MAX)]
    duration: Annotated[int, Field(ge=MovieLimits.DURATION_MIN, le=MovieLimits.DURATION_MAX)]
    release_year: Annotated[int, Field(ge=MovieLimits.RELEASE_YEAR_MIN)]
    poster_url: Annotated[str | None, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)] = None
    age_rating: Annotated[
        str | None, Field(min_length=MovieLimits.AGE_RATING_MIN, max_length=MovieLimits.AGE_RATING_MAX)] = None


class MovieBase(MovieSummaryBase):
    description: str | None = None
    premiere_date: datetime | None = None


class MovieRead(MovieBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MovieCreateDB(MovieBase):
    pass


class MovieCreateReq(BaseModel):
    title: Annotated[str, Field(min_length=MovieLimits.TITLE_MIN, max_length=MovieLimits.TITLE_MAX)]
    duration: Annotated[int, Field(ge=MovieLimits.DURATION_MIN, le=MovieLimits.DURATION_MAX)]
    release_year: Annotated[int, Field(ge=MovieLimits.RELEASE_YEAR_MIN)]
    age_rating: Annotated[
        str | None, Field(min_length=MovieLimits.AGE_RATING_MIN, max_length=MovieLimits.AGE_RATING_MAX)] = None
    description: str | None = None
    premiere_date: datetime | None = None


class MovieUpdateBase(BaseModel):
    title: Annotated[str | None, Field(min_length=MovieLimits.TITLE_MIN, max_length=MovieLimits.TITLE_MAX)] = None
    duration: Annotated[int | None, Field(ge=MovieLimits.DURATION_MIN, le=MovieLimits.DURATION_MAX)] = None
    release_year: Annotated[int | None, Field(ge=MovieLimits.RELEASE_YEAR_MIN)] = None
    age_rating: Annotated[
        str | None, Field(min_length=MovieLimits.AGE_RATING_MIN, max_length=MovieLimits.AGE_RATING_MAX)] = None
    description: str | None = None
    premiere_date: datetime | None = None


class MovieUpdateDB(MovieUpdateBase):
    slug: Annotated[str | None, Field(min_length=MovieLimits.SLUG_MIN, max_length=MovieLimits.SLUG_MAX)] = None
    poster_url: Annotated[str | None, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)] = None


class MovieUpdateReq(MovieUpdateBase):
    pass


class MovieDetail(MovieBase):
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
