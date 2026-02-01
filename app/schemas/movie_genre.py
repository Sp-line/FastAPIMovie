from pydantic import BaseModel, ConfigDict

from schemas.base import Id
from schemas.m2m import CompositeIdBase


class MovieGenreCompositeId(CompositeIdBase):
    genre_id: int
    movie_id: int


class MovieGenreBase(MovieGenreCompositeId):
    pass


class MovieGenreCreate(MovieGenreBase):
    pass


class MovieGenreUpdate(BaseModel):
    genre_id: int | None = None
    movie_id: int | None = None


class MovieGenreRead(MovieGenreBase, Id):
    model_config = ConfigDict(from_attributes=True)
