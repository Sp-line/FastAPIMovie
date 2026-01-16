from pydantic import BaseModel, ConfigDict

from constants import MovieRoleType
from schemas.person import PersonRead


class MoviePersonBase(BaseModel):
    role: MovieRoleType


class MoviePersonCreate(MoviePersonBase):
    movie_id: int
    person_id: int


class MoviePersonUpdate(MoviePersonBase):
    pass


class MoviePersonRead(MoviePersonBase):
    id: int
    movie_id: int
    person_id: int

    model_config = ConfigDict(from_attributes=True)


class MoviePersonRelatedRead(MoviePersonBase):
    person: PersonRead
