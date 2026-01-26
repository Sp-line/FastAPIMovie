from pydantic import BaseModel, ConfigDict

from constants import MovieRoleType
from schemas.m2m import CompositeIdBase
from schemas.person import PersonRead


class MoviePersonCompositeId(CompositeIdBase):
    movie_id: int
    person_id: int


class MoviePersonBase(MoviePersonCompositeId):
    role: MovieRoleType


class MoviePersonCreate(MoviePersonBase):
    pass


class MoviePersonUpdate(BaseModel):
    movie_id: int | None = None
    person_id: int | None = None
    role: MovieRoleType | None = None


class MoviePersonRead(MoviePersonBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MoviePersonRelatedRead(MoviePersonBase):
    person: PersonRead

    model_config = ConfigDict(from_attributes=True)
