from datetime import datetime

from sqlalchemy import String, Text, SmallInteger, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from constants import MOVIE_SLUG_MAX_LEN, MOVIE_TITLE_MAX_LEN, MOVIE_AGE_RATING_MAX_LEN, IMAGE_URL_MAX_LEN
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class Movie(IntIdPkMixin, Base):
    __table_args__ = (
        CheckConstraint('duration > 0 AND duration <= 600', name='check_duration_limits'),
        CheckConstraint('release_year >= 1800', name='check_release_year_min')
    )

    slug: Mapped[str] = mapped_column(String(MOVIE_SLUG_MAX_LEN), unique=True)
    title: Mapped[str] = mapped_column(String(MOVIE_TITLE_MAX_LEN))
    description: Mapped[str | None] = mapped_column(Text)
    duration: Mapped[int] = mapped_column(SmallInteger)
    age_rating: Mapped[str | None] = mapped_column(String(MOVIE_AGE_RATING_MAX_LEN))
    premiere_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    release_year: Mapped[int] = mapped_column(SmallInteger)
    poster_url: Mapped[str | None] = mapped_column(String(IMAGE_URL_MAX_LEN))
