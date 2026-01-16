from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import ImageUrlLimits, MovieShotLimits


class MovieShotBase(BaseModel):
    image_url: Annotated[str, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)]
    caption: Annotated[
        str, Field(min_length=MovieShotLimits.CAPTION_URL_MIN, max_length=MovieShotLimits.CAPTION_URL_MAX)]


class MovieShotCreate(MovieShotBase):
    movie_id: int


class MovieShotUpdate(BaseModel):
    image_url: Annotated[str | None, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)] = None
    caption: Annotated[
        str | None, Field(min_length=MovieShotLimits.CAPTION_URL_MIN,
                          max_length=MovieShotLimits.CAPTION_URL_MAX)] = None


class MovieShotRead(MovieShotBase):
    id: int
    movie_id: int

    model_config = ConfigDict(from_attributes=True)


class MovieRelatedShotRead(MovieShotBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
