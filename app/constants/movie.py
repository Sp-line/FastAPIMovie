class MovieLimits:
    TITLE_MAX: int = 255
    TITLE_MIN: int = 3

    SLUG_MAX: int = 255
    SLUG_MIN: int = 3

    DURATION_MIN: int = 1
    DURATION_MAX: int = 600

    AGE_RATING_MAX: int = 10
    AGE_RATING_MIN: int = 2
    AGE_RATING_REQ: bool = False

    POSTER_URL_REQ: bool = False

    PREMIER_DATE_REQ: bool = False

    DESCRIPTION_REQ: bool = False

    RELEASE_YEAR_MIN: int = 1800