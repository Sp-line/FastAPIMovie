from pydantic import BaseModel, ConfigDict

from constants import MovieRoleType
from schemas.base import Id
from schemas.event import EventSchemas
from schemas.m2m import CompositeIdBase
from schemas.person import PersonRead


class MoviePersonCompositeId(CompositeIdBase):
    movie_id: int
    person_id: int


class MoviePersonBase(MoviePersonCompositeId):
    role: MovieRoleType


class MoviePersonCreate(MoviePersonBase):
    pass


class MoviePersonUpdateBase(BaseModel):
    role: MovieRoleType | None = None


class MoviePersonUpdateDB(MoviePersonUpdateBase):
    movie_id: int | None = None
    person_id: int | None = None


class MoviePersonUpdateReq(MoviePersonUpdateBase):
    pass


class MoviePersonRead(MoviePersonBase, Id):
    model_config = ConfigDict(from_attributes=True)


class MoviePersonRelatedRead(MoviePersonBase):
    person: PersonRead

    model_config = ConfigDict(from_attributes=True)


class MoviePersonCreateEvent(MoviePersonRead):
    model_config = ConfigDict(from_attributes=True)


class MoviePersonUpdateEvent(MoviePersonBase, Id):
    model_config = ConfigDict(from_attributes=True)


class MoviePersonDeleteEvent(MoviePersonCompositeId, Id):
    model_config = ConfigDict(from_attributes=True)


movie_person_event_schemas = EventSchemas[
    MoviePersonCreateEvent,
    MoviePersonUpdateEvent,
    MoviePersonDeleteEvent
](
    create=MoviePersonCreateEvent,
    update=MoviePersonUpdateEvent,
    delete=MoviePersonDeleteEvent
)
