from pydantic import BaseModel, ConfigDict

from schemas.base import Id
from schemas.event import EventSchemas
from schemas.m2m import CompositeIdBase


class MovieCountryCompositeId(CompositeIdBase):
    country_id: int
    movie_id: int


class MovieCountryBase(MovieCountryCompositeId):
    pass


class MovieCountryCreate(MovieCountryBase):
    pass


class MovieCountryUpdate(BaseModel):
    country_id: int | None = None
    movie_id: int | None = None


class MovieCountryRead(MovieCountryBase, Id):
    model_config = ConfigDict(from_attributes=True)


class MovieCountryCreateEvent(MovieCountryRead):
    model_config = ConfigDict(from_attributes=True)


class MovieCountryUpdateEvent(MovieCountryUpdate, Id):
    model_config = ConfigDict(from_attributes=True)


class MovieCountryDeleteEvent(MovieCountryCompositeId, Id):
    model_config = ConfigDict(from_attributes=True)


movie_country_event_schemas = EventSchemas[
    MovieCountryCreateEvent,
    MovieCountryUpdateEvent,
    MovieCountryDeleteEvent
](
    create=MovieCountryCreateEvent,
    update=MovieCountryUpdateEvent,
    delete=MovieCountryDeleteEvent
)
