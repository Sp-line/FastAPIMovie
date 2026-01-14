from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class MovieGenreAssociation(IntIdPkMixin, Base):
    __table_args__ = (
        UniqueConstraint("movie_id", "genre_id", name="uq_movie_genre"),
    )

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id", ondelete="RESTRICT"))
