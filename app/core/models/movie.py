from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, SmallInteger, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import ImageUrlLimits, MovieLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import MovieShot, MoviePersonAssociation, MovieCountryAssociation, MovieGenreAssociation, Genre, \
        Country


class Movie(IntIdPkMixin, Base):
    __table_args__ = (
        CheckConstraint(
            f"duration >= {MovieLimits.DURATION_MIN} AND duration <= {MovieLimits.DURATION_MAX}",
            name='check_duration_limits'
        ),
        CheckConstraint(
            f"release_year >= {MovieLimits.RELEASE_YEAR_MIN}",
            name='check_release_year_min'
        ),
        CheckConstraint(
            f"char_length(title) > {MovieLimits.TITLE_MIN}",
            name="check_movie_title_not_empty"
        ),
        CheckConstraint(
            f"char_length(slug) > {MovieLimits.SLUG_MIN}",
            name="check_movie_slug_not_empty"
        ),
        CheckConstraint(
            f"char_length(poster_url) > {ImageUrlLimits.MIN}",
            name="check_movie_poster_url_not_empty"
        ),
        CheckConstraint(
            f"char_length(age_rating) > {MovieLimits.AGE_RATING_MIN}",
            name="check_movie_age_rating_not_empty"
        ),
    )

    slug: Mapped[str] = mapped_column(String(MovieLimits.SLUG_MAX), unique=True)
    title: Mapped[str] = mapped_column(String(MovieLimits.TITLE_MAX))
    description: Mapped[str | None] = mapped_column(Text)
    duration: Mapped[int] = mapped_column(SmallInteger)
    age_rating: Mapped[str | None] = mapped_column(String(MovieLimits.AGE_RATING_MAX))
    premiere_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    release_year: Mapped[int] = mapped_column(SmallInteger)
    poster_url: Mapped[str | None] = mapped_column(String(ImageUrlLimits.MAX))

    shots: Mapped[list["MovieShot"]] = relationship(
        back_populates="movie",
        cascade="all, delete-orphan"
    )
    person_associations: Mapped[list["MoviePersonAssociation"]] = relationship(
        back_populates="movie",
        cascade="all, delete-orphan"
    )
    genre_associations: Mapped[list["MovieGenreAssociation"]] = relationship(
        back_populates="movie",
        cascade="all, delete-orphan",
    )
    country_associations: Mapped[list["MovieCountryAssociation"]] = relationship(
        back_populates="movie",
        cascade="all, delete-orphan",
    )
    genres: Mapped[list["Genre"]] = relationship(
        secondary="movie_genre_associations",
        back_populates="movies",
        viewonly=True,
        overlaps="genre_associations"
    )
    countries: Mapped[list["Country"]] = relationship(
        secondary="movie_country_associations",
        back_populates="movies",
        viewonly=True,
        overlaps="country_associations"
    )
