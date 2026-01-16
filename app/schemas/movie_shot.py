from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import IMAGE_URL_MAX_LEN, MOVIE_SHOT_CAPTION_URL_MAX_LEN
from constants.movie_shot import MOVIE_SHOT_CAPTION_URL_MIN_LEN


class MovieShotBase(BaseModel):
    image_url: Annotated[str, Field(max_length=IMAGE_URL_MAX_LEN)]
    caption: Annotated[str, Field(min_length=MOVIE_SHOT_CAPTION_URL_MIN_LEN, max_length=MOVIE_SHOT_CAPTION_URL_MAX_LEN)]


class MovieShotCreate(MovieShotBase):
    movie_id: int


class MovieShotUpdate(BaseModel):
    image_url: Annotated[str | None, Field(max_length=IMAGE_URL_MAX_LEN)] = None
    caption: Annotated[
        str | None, Field(min_length=MOVIE_SHOT_CAPTION_URL_MIN_LEN, max_length=MOVIE_SHOT_CAPTION_URL_MAX_LEN)] = None


class MovieShotRead(MovieShotBase):
    id: int
    movie_id: int

    model_config = ConfigDict(from_attributes=True)


class MovieRelatedShotRead(MovieShotBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
