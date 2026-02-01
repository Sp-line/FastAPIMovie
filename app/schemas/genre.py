from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from constants import GenreLimits
from schemas.base import Id


class GenreBase(BaseModel):
    name: Annotated[str, Field(min_length=GenreLimits.NAME_MIN, max_length=GenreLimits.NAME_MAX)]
    slug: Annotated[str, Field(min_length=GenreLimits.SLUG_MIN, max_length=GenreLimits.SLUG_MAX)]


class GenreCreateDB(GenreBase):
    pass


class GenreCreateReq(BaseModel):
    name: Annotated[str, Field(min_length=GenreLimits.NAME_MIN, max_length=GenreLimits.NAME_MAX)]


class GenreRead(GenreBase, Id):
    model_config = ConfigDict(from_attributes=True)


class GenreUpdateBase(BaseModel):
    name: Annotated[str | None, Field(min_length=GenreLimits.NAME_MIN, max_length=GenreLimits.NAME_MAX)] = None


class GenreUpdateDB(GenreUpdateBase):
    slug: Annotated[str | None, Field(min_length=GenreLimits.SLUG_MIN, max_length=GenreLimits.SLUG_MAX)] = None


class GenreUpdateReq(GenreUpdateBase):
    pass
