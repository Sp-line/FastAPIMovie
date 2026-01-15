from pydantic import BaseModel, ConfigDict

from constants import MovieRoleType


class MoviePersonBase(BaseModel):
    role: MovieRoleType


class MoviePersonCreate(MoviePersonBase):
    movie_id: int
    person_id: int


class MoviePersonUpdate(BaseModel):
    role: MovieRoleType


class MoviePersonRead(MoviePersonBase):
    id: int
    movie_id: int
    person_id: int

    model_config = ConfigDict(from_attributes=True)
