from pydantic import BaseModel, ConfigDict

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


class MovieCountryRead(MovieCountryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

