import enum


class MovieRoleType(enum.StrEnum):
    ACTOR = "actor"
    DIRECTOR = "director"
    WRITER = "writer"
    PRODUCER = "producer"


PERSON_FULL_NAME_MAX_LEN = 150
PERSON_SLUG_MAX_LEN = 150
PERSON_FULL_NAME_MIN_LEN = 3
PERSON_SLUG_MIN_LEN = 3
PERSON_PHOTO_URL_REQUIRED = False