from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from constants import COUNTRY_NAME_MAX_LEN, COUNTRY_SLUG_MAX_LEN
from constants.country import COUNTRY_NAME_MIN_LEN, COUNTRY_SLUG_MIN_LEN


class CountryBase(BaseModel):
    name: Annotated[str, Field(min_length=COUNTRY_NAME_MIN_LEN, max_length=COUNTRY_NAME_MAX_LEN)]
    slug: Annotated[str, Field(min_length=COUNTRY_SLUG_MIN_LEN, max_length=COUNTRY_SLUG_MAX_LEN)]


class CountryCreate(CountryBase):
    pass


class CountryUpdate(BaseModel):
    name: Annotated[str | None, Field(min_length=COUNTRY_NAME_MIN_LEN, max_length=COUNTRY_NAME_MAX_LEN)] = None
    slug: Annotated[str | None, Field(min_length=COUNTRY_SLUG_MIN_LEN, max_length=COUNTRY_SLUG_MAX_LEN)] = None


class CountryRead(CountryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
