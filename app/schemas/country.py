from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from constants import CountryLimits


class CountryBase(BaseModel):
    name: Annotated[str, Field(min_length=CountryLimits.NAME_MIN, max_length=CountryLimits.NAME_MAX)]
    slug: Annotated[str, Field(min_length=CountryLimits.SLUG_MIN, max_length=CountryLimits.SLUG_MAX)]


class CountryCreate(CountryBase):
    pass


class CountryUpdate(BaseModel):
    name: Annotated[str | None, Field(min_length=CountryLimits.NAME_MIN, max_length=CountryLimits.NAME_MAX)] = None
    slug: Annotated[str | None, Field(min_length=CountryLimits.SLUG_MIN, max_length=CountryLimits.SLUG_MAX)] = None


class CountryRead(CountryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
