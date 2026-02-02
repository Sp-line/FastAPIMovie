from pydantic import BaseModel, ConfigDict

from schemas.base import Id
from schemas.event import EventSchemas
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


class MovieGenreCreateEvent(MovieGenreRead):
    model_config = ConfigDict(from_attributes=True)


class MovieGenreUpdateEvent(MovieGenreUpdate, Id):
    model_config = ConfigDict(from_attributes=True)


movie_genre_event_schemas = EventSchemas[
    MovieGenreCreateEvent,
    MovieGenreUpdateEvent,
    Id
](
    create=MovieGenreCreateEvent,
    update=MovieGenreUpdateEvent,
    delete=Id
)
