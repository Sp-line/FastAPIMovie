from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Movie, Country


class MovieCountryAssociation(IntIdPkMixin, Base):
    __table_args__ = (UniqueConstraint("country_id", "movie_id", name="uq_country_movie"),)

    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="RESTRICT"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"))

    movie: Mapped["Movie"] = relationship(back_populates="country_associations")
    country: Mapped["Country"] = relationship(back_populates="movie_associations")