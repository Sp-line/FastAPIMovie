from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import MOVIE_SHOT_CAPTION_URL_MAX_LEN, IMAGE_URL_MAX_LEN
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Movie


class MovieShot(IntIdPkMixin, Base):
    image_url: Mapped[str] = mapped_column(String(IMAGE_URL_MAX_LEN))
    caption: Mapped[str] = mapped_column(String(MOVIE_SHOT_CAPTION_URL_MAX_LEN))

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"))
    movie: Mapped["Movie"] = relationship(back_populates="shots")
