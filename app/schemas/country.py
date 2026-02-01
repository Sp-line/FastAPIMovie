from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from constants import CountryLimits
from schemas.base import Id


class CountryBase(BaseModel):
    name: Annotated[str, Field(min_length=CountryLimits.NAME_MIN, max_length=CountryLimits.NAME_MAX)]
    slug: Annotated[str, Field(min_length=CountryLimits.SLUG_MIN, max_length=CountryLimits.SLUG_MAX)]


class CountryCreateDB(CountryBase):
    pass


class CountryCreateReq(BaseModel):
    name: Annotated[str, Field(min_length=CountryLimits.NAME_MIN, max_length=CountryLimits.NAME_MAX)]


class CountryRead(CountryBase, Id):
    model_config = ConfigDict(from_attributes=True)


class CountryUpdateBase(BaseModel):
    name: Annotated[str | None, Field(min_length=CountryLimits.NAME_MIN, max_length=CountryLimits.NAME_MAX)] = None


class CountryUpdateDB(CountryUpdateBase):
    slug: Annotated[str | None, Field(min_length=CountryLimits.SLUG_MIN, max_length=CountryLimits.SLUG_MAX)] = None


class CountryUpdateReq(CountryUpdateBase):
    pass


class CountryCreateEvent(CountryRead):
    name: str

    model_config = ConfigDict(from_attributes=True)


class CountryUpdateEvent(CountryUpdateDB, Id):
    model_config = ConfigDict(from_attributes=True)
