from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, SmallInteger, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import MOVIE_SLUG_MAX_LEN, MOVIE_TITLE_MAX_LEN, MOVIE_AGE_RATING_MAX_LEN, IMAGE_URL_MAX_LEN, \
    MOVIE_DURATION_MIN_VALUE, MOVIE_DURATION_MAX_VALUE, IMAGE_URL_MIN_LEN, MOVIE_RELEASE_YEAR_MIN_VALUE, \
    MOVIE_TITLE_MIN_LEN, MOVIE_SLUG_MIN_LEN, MOVIE_AGE_RATING_MIN_LEN
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import MovieShot, MoviePersonAssociation, Genre, Country


class Movie(IntIdPkMixin, Base):
    __table_args__ = (
        CheckConstraint(
            f"duration >= {MOVIE_DURATION_MIN_VALUE} AND duration <= {MOVIE_DURATION_MAX_VALUE}",
            name='check_duration_limits'
        ),
        CheckConstraint(
            f"release_year >= {MOVIE_RELEASE_YEAR_MIN_VALUE}",
            name='check_release_year_min'
        ),
        CheckConstraint(
            f"char_length(title) > {MOVIE_TITLE_MIN_LEN}",
            name="check_movie_title_not_empty"
        ),
        CheckConstraint(
            f"char_length(slug) > {MOVIE_SLUG_MIN_LEN}",
            name="check_movie_slug_not_empty"
        ),
        CheckConstraint(
            f"char_length(poster_url) > {IMAGE_URL_MIN_LEN}",
            name="check_movie_poster_url_not_empty"
        ),
        CheckConstraint(
            f"char_length(age_rating) > {MOVIE_AGE_RATING_MIN_LEN}",
            name="check_movie_age_rating_not_empty"
        ),
    )

    slug: Mapped[str] = mapped_column(String(MOVIE_SLUG_MAX_LEN), unique=True)
    title: Mapped[str] = mapped_column(String(MOVIE_TITLE_MAX_LEN))
    description: Mapped[str | None] = mapped_column(Text)
    duration: Mapped[int] = mapped_column(SmallInteger)
    age_rating: Mapped[str | None] = mapped_column(String(MOVIE_AGE_RATING_MAX_LEN))
    premiere_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    release_year: Mapped[int] = mapped_column(SmallInteger)
    poster_url: Mapped[str | None] = mapped_column(String(IMAGE_URL_MAX_LEN))

    shots: Mapped[list["MovieShot"]] = relationship(
        back_populates="movie",
        cascade="all, delete-orphan"
    )
    person_associations: Mapped[list["MoviePersonAssociation"]] = relationship(
        back_populates="movie",
        cascade="all, delete-orphan"
    )
    genres: Mapped[list["Genre"]] = relationship(
        secondary="movie_genres",
        back_populates="movies"
    )
    countries: Mapped[list["Country"]] = relationship(
        secondary="movie_country_associations",
        back_populates="movies"
    )
