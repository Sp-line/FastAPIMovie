from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class MovieCountryAssociation(IntIdPkMixin, Base):
    __table_args__ = (UniqueConstraint("country_id", "movie_id", name="uq_country_movie"),)

    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="RESTRICT"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"))