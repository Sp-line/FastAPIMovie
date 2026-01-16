import enum


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
