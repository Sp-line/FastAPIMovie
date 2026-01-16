from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from constants import GenreLimits


class GenreBase(BaseModel):
    name: Annotated[str, Field(min_length=GenreLimits.NAME_MIN, max_length=GenreLimits.NAME_MAX)]
    slug: Annotated[str, Field(min_length=GenreLimits.SLUG_MIN, max_length=GenreLimits.SLUG_MAX)]


class GenreCreate(GenreBase):
    pass


class GenreUpdate(BaseModel):
    name: Annotated[str | None, Field(min_length=GenreLimits.NAME_MIN, max_length=GenreLimits.NAME_MAX)] = None
    slug: Annotated[str | None, Field(min_length=GenreLimits.SLUG_MIN, max_length=GenreLimits.SLUG_MAX)] = None


class GenreRead(GenreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
