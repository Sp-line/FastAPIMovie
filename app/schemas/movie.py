from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import MovieLimits, ImageUrlLimits
from constants.movie import AgeRating
from filters.base import RangeFilter, TermFilter, FilterStrategy, WeightedTermFilter
from filters.types import RangeOperator
from schemas.base import Id, Pagination
from schemas.cache import ModelCacheConfig
from schemas.country import CountryRead
from schemas.event import EventSchemas
from schemas.genre import GenreRead
from schemas.movie_person import MoviePersonRelatedRead
from schemas.movie_shot import MovieRelatedShotRead


class MovieSummaryBase(BaseModel):
    title: Annotated[str, Field(min_length=MovieLimits.TITLE_MIN, max_length=MovieLimits.TITLE_MAX)]
    slug: Annotated[str, Field(min_length=MovieLimits.SLUG_MIN, max_length=MovieLimits.SLUG_MAX)]
    duration: Annotated[int, Field(ge=MovieLimits.DURATION_MIN, le=MovieLimits.DURATION_MAX)]
    release_year: Annotated[int, Field(ge=MovieLimits.RELEASE_YEAR_MIN)]
    poster_url: Annotated[str | None, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)] = None
    age_rating: AgeRating | None = None


class MovieBase(MovieSummaryBase):
    description: str | None = None
    premiere_date: datetime | None = None


class MovieRead(MovieBase, Id):
    model_config = ConfigDict(from_attributes=True)


class MovieCreateDB(MovieBase):
    pass


class MovieCreateReq(BaseModel):
    title: Annotated[str, Field(min_length=MovieLimits.TITLE_MIN, max_length=MovieLimits.TITLE_MAX)]
    duration: Annotated[int, Field(ge=MovieLimits.DURATION_MIN, le=MovieLimits.DURATION_MAX)]
    release_year: Annotated[int, Field(ge=MovieLimits.RELEASE_YEAR_MIN)]
    age_rating: AgeRating | None = None
    description: str | None = None
    premiere_date: datetime | None = None


class MovieUpdateBase(BaseModel):
    title: Annotated[str | None, Field(min_length=MovieLimits.TITLE_MIN, max_length=MovieLimits.TITLE_MAX)] = None
    duration: Annotated[int | None, Field(ge=MovieLimits.DURATION_MIN, le=MovieLimits.DURATION_MAX)] = None
    release_year: Annotated[int | None, Field(ge=MovieLimits.RELEASE_YEAR_MIN)] = None
    age_rating: AgeRating | None = None
    description: str | None = None
    premiere_date: datetime | None = None


class MovieUpdateDB(MovieUpdateBase):
    slug: Annotated[str | None, Field(min_length=MovieLimits.SLUG_MIN, max_length=MovieLimits.SLUG_MAX)] = None
    poster_url: Annotated[str | None, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)] = None


class MovieUpdateReq(MovieUpdateBase):
    pass


class MovieDetail(MovieRead):
    genres: Annotated[list[GenreRead], Field(default_factory=list)]
    countries: Annotated[list[CountryRead], Field(default_factory=list)]
    shots: Annotated[list[MovieRelatedShotRead], Field(default_factory=list)]
    person_associations: Annotated[list[MoviePersonRelatedRead], Field(default_factory=list)]

    model_config = ConfigDict(from_attributes=True)


class MovieList(MovieSummaryBase):
    id: int

    genres: Annotated[list[GenreRead], Field(default_factory=list)]

    model_config = ConfigDict(from_attributes=True)


class MovieCreateEvent(MovieRead):
    model_config = ConfigDict(from_attributes=True)


class MovieUpdateEvent(MovieUpdateDB, Id):
    model_config = ConfigDict(from_attributes=True)


class MovieCacheConfig(ModelCacheConfig):
    list_summary_key: str = "{table_name}:list:summary:skip={skip}:limit={limit}"
    list_summary_ttl: int = 14400
    detail_key: str = "{table_name}:detail:id={obj_id}"
    detail_ttl: int = 14400


class MovieFilter(Pagination):
    duration_gte: Annotated[int | None, Field(ge=MovieLimits.DURATION_MIN)] = None
    duration_lte: Annotated[int | None, Field(le=MovieLimits.DURATION_MAX)] = None
    release_year_gte: Annotated[int | None, Field(ge=MovieLimits.RELEASE_YEAR_MIN)] = None
    release_year_lte: int | None = None
    age_rating: AgeRating | None = None
    genre_ids: list[int] | None = None
    country_ids: list[int] | None = None
    person_ids: list[int] | None = None


class MovieFilterRegistry(BaseModel):
    duration_gte: FilterStrategy = RangeFilter("duration", RangeOperator.GTE)
    duration_lte: FilterStrategy = RangeFilter("duration", RangeOperator.LTE)
    release_year_gte: FilterStrategy = RangeFilter("release_year", RangeOperator.GTE)
    release_year_lte: FilterStrategy = RangeFilter("release_year", RangeOperator.LTE)
    age_rating: FilterStrategy = TermFilter("age_rating")
    genre_ids: FilterStrategy = WeightedTermFilter("genre_ids")
    country_ids: FilterStrategy = WeightedTermFilter("country_ids")
    person_ids: FilterStrategy = WeightedTermFilter("person_ids")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class MovieSearchRead(Id):
    title: str
    slug: str

    model_config = ConfigDict(from_attributes=True)


class MovieElasticSchema(MovieRead):
    genre_ids: Annotated[list[int], Field(default_factory=list)]
    country_ids: Annotated[list[int], Field(default_factory=list)]
    person_ids: Annotated[list[int], Field(default_factory=list)]

    model_config = ConfigDict(from_attributes=True)


class MovieElasticUpdateSchema(MovieUpdateDB):
    genre_ids: list[int] | None = None
    country_ids: list[int] | None = None
    person_ids: list[int] | None = None

    model_config = ConfigDict(from_attributes=True)


class MovieElasticBulkUpdateSchema(MovieElasticUpdateSchema, Id):
    model_config = ConfigDict(from_attributes=True)


movie_event_schemas = EventSchemas[
    MovieCreateEvent,
    MovieUpdateEvent,
    Id
](
    create=MovieCreateEvent,
    update=MovieUpdateEvent,
    delete=Id
)
