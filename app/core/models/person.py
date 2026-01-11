from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from constants import PERSON_FULL_NAME_MAX_LEN, PERSON_SLUG_MAX_LEN, IMAGE_URL_MAX_LEN
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class Person(IntIdPkMixin, Base):
    full_name: Mapped[str] = mapped_column(String(PERSON_FULL_NAME_MAX_LEN))
    slug: Mapped[str] = mapped_column(String(PERSON_SLUG_MAX_LEN), unique=True)
    photo_url: Mapped[str | None] = mapped_column(String(IMAGE_URL_MAX_LEN))
