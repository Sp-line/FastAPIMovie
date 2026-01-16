import enum

PERSON_FULL_NAME_MAX_LEN = 150
PERSON_SLUG_MAX_LEN = 150
PERSON_FULL_NAME_MIN_LEN = 3
PERSON_SLUG_MIN_LEN = 3
PERSON_PHOTO_URL_REQUIRED = False


class MovieRoleType(enum.StrEnum):
    ACTOR = "actor"
    DIRECTOR = "director"
    WRITER = "writer"
    PRODUCER = "producer"


class PersonLimits:
    FULL_NAME_MAX: int = 150
    FULL_NAME_MIN: int = 3

    SLUG_MAX: int = 150
    SLUG_MIN: int = 3

    PHOTO_URL_REQ: bool = False
