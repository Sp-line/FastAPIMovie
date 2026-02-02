from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import ImageUrlLimits, MovieShotLimits
from schemas.base import Id
from schemas.event import EventSchemas


class MovieShotBase(BaseModel):
    image_url: Annotated[str | None, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)] = None
    caption: Annotated[
        str, Field(min_length=MovieShotLimits.CAPTION_URL_MIN, max_length=MovieShotLimits.CAPTION_URL_MAX)]


class MovieShotCreateDB(MovieShotBase):
    movie_id: int


class MovieShotCreateReq(BaseModel):
    caption: Annotated[
        str, Field(min_length=MovieShotLimits.CAPTION_URL_MIN, max_length=MovieShotLimits.CAPTION_URL_MAX)]
    movie_id: int


class MovieShotUpdateDB(BaseModel):
    image_url: Annotated[str | None, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)] = None
    caption: Annotated[str | None, Field(min_length=MovieShotLimits.CAPTION_URL_MIN,
                                         max_length=MovieShotLimits.CAPTION_URL_MAX)] = None


class MovieShotUpdateReq(BaseModel):
    caption: Annotated[str | None, Field(min_length=MovieShotLimits.CAPTION_URL_MIN,
                                         max_length=MovieShotLimits.CAPTION_URL_MAX)] = None


class MovieShotRead(MovieShotBase, Id):
    movie_id: int

    model_config = ConfigDict(from_attributes=True)


class MovieRelatedShotRead(MovieShotBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MovieShotCreateEvent(MovieShotRead):
    model_config = ConfigDict(from_attributes=True)


class MovieShotUpdateEvent(MovieShotUpdateDB, Id):
    movie_id: int

    model_config = ConfigDict(from_attributes=True)


movie_shot_event_schemas = EventSchemas[
    MovieShotCreateEvent,
    MovieShotUpdateEvent,
    Id
](
    create=MovieShotCreateEvent,
    update=MovieShotUpdateEvent,
    delete=Id
)
