from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import COUNTRY_NAME_MAX_LEN, COUNTRY_SLUG_MAX_LEN
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Movie


class Country(IntIdPkMixin, Base):
    __tablename__ = "countries"

    name: Mapped[str] = mapped_column(String(COUNTRY_NAME_MAX_LEN), unique=True)
    slug: Mapped[str] = mapped_column(String(COUNTRY_SLUG_MAX_LEN), unique=True)

    movies: Mapped[list["Movie"]] = relationship(
        secondary="movie_country_associations",
        back_populates="countries"
    )