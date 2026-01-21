from typing import TYPE_CHECKING

from sqlalchemy import String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import GenreLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Movie


class Genre(IntIdPkMixin, Base):
    __table_args__ = (
        CheckConstraint(
            f"char_length(name) >= {GenreLimits.NAME_MIN}",
            name="check_genre_name_min_len"
        ),
        CheckConstraint(
            f"char_length(slug) >= {GenreLimits.SLUG_MIN}",
            name="check_genre_slug_min_len"
        ),
    )

    name: Mapped[str] = mapped_column(String(GenreLimits.NAME_MAX), unique=True)
    slug: Mapped[str] = mapped_column(String(GenreLimits.SLUG_MAX), unique=True)

    movies: Mapped[list["Movie"]] = relationship(
        secondary="movie_genre_associations",
        back_populates="genres"
    )
