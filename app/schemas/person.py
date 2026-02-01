from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import ImageUrlLimits, PersonLimits
from schemas.base import Id


class PersonBase(BaseModel):
    full_name: Annotated[str, Field(min_length=PersonLimits.FULL_NAME_MIN, max_length=PersonLimits.FULL_NAME_MAX)]
    slug: Annotated[str, Field(min_length=PersonLimits.SLUG_MIN, max_length=PersonLimits.SLUG_MAX)]
    photo_url: Annotated[str | None, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)] = None


class PersonCreateDB(PersonBase):
    pass


class PersonCreateReq(BaseModel):
    full_name: Annotated[str, Field(min_length=PersonLimits.FULL_NAME_MIN, max_length=PersonLimits.FULL_NAME_MAX)]


class PersonUpdateBase(BaseModel):
    full_name: Annotated[
        str | None, Field(min_length=PersonLimits.FULL_NAME_MIN, max_length=PersonLimits.FULL_NAME_MAX)] = None


class PersonUpdateDB(PersonUpdateBase):
    photo_url: Annotated[str | None, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)] = None


class PersonUpdateReq(PersonUpdateBase):
    pass


class PersonRead(PersonBase, Id):
    model_config = ConfigDict(from_attributes=True)
