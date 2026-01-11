from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import MovieRoleType
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Movie, Person


class MoviePersonAssociation(IntIdPkMixin, Base):
    __table_args__ = (
        UniqueConstraint("person_id", "movie_id", "role", name="uq_movie_person_role"),
    )

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"))
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id", ondelete="RESTRICT"))
    role: Mapped[MovieRoleType] = mapped_column(SAEnum(MovieRoleType))

    movie: Mapped["Movie"] = relationship(back_populates="person_associations")
    person: Mapped["Person"] = relationship(back_populates="movie_associations")