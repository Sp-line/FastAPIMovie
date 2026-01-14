from typing import TypeVar

from core.models.mixins.int_id_pk import IntIdPkMixin

ModelType = TypeVar("ModelType", bound=IntIdPkMixin)
