from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from constants import CountryLimits


class CountryBase(BaseModel):
    name: Annotated[str, Field(min_length=CountryLimits.NAME_MIN, max_length=CountryLimits.NAME_MAX)]
    slug: Annotated[str, Field(min_length=CountryLimits.SLUG_MIN, max_length=CountryLimits.SLUG_MAX)]


class CountryCreateDB(CountryBase):
    pass


class CountryCreateReq(CountryBase):
    pass


class CountryRead(CountryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CountryUpdateBase(BaseModel):
    name: Annotated[str | None, Field(min_length=CountryLimits.NAME_MIN, max_length=CountryLimits.NAME_MAX)] = None


class CountryUpdateDB(CountryUpdateBase):
    slug: Annotated[str | None, Field(min_length=CountryLimits.SLUG_MIN, max_length=CountryLimits.SLUG_MAX)] = None


class CountryUpdateReq(CountryUpdateBase):
    pass
