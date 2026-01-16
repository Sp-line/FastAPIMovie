from typing import TYPE_CHECKING

from sqlalchemy import String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import COUNTRY_NAME_MAX_LEN, COUNTRY_SLUG_MAX_LEN
from constants.country import COUNTRY_NAME_MIN_LEN, COUNTRY_SLUG_MIN_LEN
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Movie


class Country(IntIdPkMixin, Base):
    __tablename__ = "countries"
    __table_args__ = (
        CheckConstraint(
            f"char_length(name) >= {COUNTRY_NAME_MIN_LEN}",
            name="check_country_name_min_len"
        ),
        CheckConstraint(
            f"char_length(slug) >= {COUNTRY_SLUG_MIN_LEN}",
            name="check_country_slug_min_len"
        ),
    )

    name: Mapped[str] = mapped_column(String(COUNTRY_NAME_MAX_LEN), unique=True)
    slug: Mapped[str] = mapped_column(String(COUNTRY_SLUG_MAX_LEN), unique=True)

    movies: Mapped[list["Movie"]] = relationship(
        secondary="movie_country_associations",
        back_populates="countries"
    )