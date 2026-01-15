from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from constants import GENRE_NAME_MAX_LEN, GENRE_SLUG_MAX_LEN
from constants.genre import GENRE_NAME_MIN_LEN, GENRE_SLUG_MIN_LEN


class GenreBase(BaseModel):
    name: Annotated[str, Field(min_length=GENRE_NAME_MIN_LEN, max_length=GENRE_NAME_MAX_LEN)]
    slug: Annotated[str, Field(min_length=GENRE_SLUG_MIN_LEN, max_length=GENRE_SLUG_MAX_LEN)]


class GenreCreate(GenreBase):
    pass


class GenreUpdate(BaseModel):
    name: Annotated[str | None, Field(min_length=GENRE_NAME_MIN_LEN, max_length=GENRE_NAME_MAX_LEN)] = None
    slug: Annotated[str | None, Field(min_length=GENRE_SLUG_MIN_LEN, max_length=GENRE_SLUG_MAX_LEN)] = None


class GenreRead(GenreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
