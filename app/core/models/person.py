from typing import TYPE_CHECKING

from sqlalchemy import String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import PERSON_FULL_NAME_MAX_LEN, PERSON_SLUG_MAX_LEN, PERSON_FULL_NAME_MIN_LEN, PERSON_SLUG_MIN_LEN, \
    ImageUrlLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import MoviePersonAssociation


class Person(IntIdPkMixin, Base):
    __table_args__ = (
        CheckConstraint(
            f"char_length(full_name) >= {PERSON_FULL_NAME_MIN_LEN}",
            name="check_person_full_name_min_len"
        ),
        CheckConstraint(
            f"char_length(slug) >= {PERSON_SLUG_MIN_LEN}",
            name="check_person_slug_min_len"
        ),
        CheckConstraint(
            f"char_length(photo_url) > {ImageUrlLimits.MIN}",
            name="check_person_photo_url_not_empty"
        ),
    )

    full_name: Mapped[str] = mapped_column(String(PERSON_FULL_NAME_MAX_LEN))
    slug: Mapped[str] = mapped_column(String(PERSON_SLUG_MAX_LEN), unique=True)
    photo_url: Mapped[str | None] = mapped_column(String(ImageUrlLimits.MAX))

    movie_associations: Mapped[list["MoviePersonAssociation"]] = relationship(back_populates="person")
