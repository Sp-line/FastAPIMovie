from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import PERSON_FULL_NAME_MAX_LEN, PERSON_SLUG_MAX_LEN, IMAGE_URL_MAX_LEN
from constants.person import PERSON_FULL_NAME_MIN_LEN, PERSON_SLUG_MIN_LEN


class PersonBase(BaseModel):
    full_name: Annotated[str, Field(min_length=PERSON_FULL_NAME_MIN_LEN, max_length=PERSON_FULL_NAME_MAX_LEN)]
    slug: Annotated[str, Field(min_length=PERSON_SLUG_MIN_LEN, max_length=PERSON_SLUG_MAX_LEN)]
    photo_url: Annotated[str | None, Field(max_length=IMAGE_URL_MAX_LEN)] = None


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    full_name: Annotated[str | None, Field(min_length=PERSON_FULL_NAME_MIN_LEN, max_length=PERSON_FULL_NAME_MAX_LEN)] = None
    slug: Annotated[str | None, Field(min_length=PERSON_SLUG_MIN_LEN, max_length=PERSON_SLUG_MAX_LEN)] = None
    photo_url: Annotated[str | None, Field(max_length=IMAGE_URL_MAX_LEN)] = None


class PersonRead(PersonBase):
    id: int

    model_config = ConfigDict(from_attributes=True)



