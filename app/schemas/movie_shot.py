from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import ImageUrlLimits, MovieShotLimits


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


class MovieShotRead(MovieShotBase):
    id: int
    movie_id: int

    model_config = ConfigDict(from_attributes=True)


class MovieRelatedShotRead(MovieShotBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
