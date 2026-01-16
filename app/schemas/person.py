from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import ImageUrlLimits, PersonLimits


class PersonBase(BaseModel):
    full_name: Annotated[str, Field(min_length=PersonLimits.FULL_NAME_MIN, max_length=PersonLimits.FULL_NAME_MIN)]
    slug: Annotated[str, Field(min_length=PersonLimits.SLUG_MIN, max_length=PersonLimits.SLUG_MAX)]
    photo_url: Annotated[str | None, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)] = None


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    full_name: Annotated[
        str | None, Field(min_length=PersonLimits.FULL_NAME_MIN, max_length=PersonLimits.FULL_NAME_MIN)] = None
    slug: Annotated[str | None, Field(min_length=PersonLimits.SLUG_MIN, max_length=PersonLimits.SLUG_MAX)] = None
    photo_url: Annotated[str | None, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)] = None


class PersonRead(PersonBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
