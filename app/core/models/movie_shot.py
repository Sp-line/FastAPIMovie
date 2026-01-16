from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import MOVIE_SHOT_CAPTION_URL_MAX_LEN, MOVIE_SHOT_CAPTION_URL_MIN_LEN, ImageUrlLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Movie


class MovieShot(IntIdPkMixin, Base):
    __table_args__ = (
        CheckConstraint(
            f"char_length(caption) >= {MOVIE_SHOT_CAPTION_URL_MIN_LEN}",
            name="check_movie_shot_caption_min_len"
        ),
        CheckConstraint(
            f"char_length(image_url) > {ImageUrlLimits.MIN}",
            name="check_movie_shot_image_url_not_empty"
        ),
    )

    image_url: Mapped[str] = mapped_column(String(ImageUrlLimits.MAX))
    caption: Mapped[str] = mapped_column(String(MOVIE_SHOT_CAPTION_URL_MAX_LEN))

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"))
    movie: Mapped["Movie"] = relationship(back_populates="shots")
