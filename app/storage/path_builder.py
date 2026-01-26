from slugify import slugify

from exceptions.s3 import FilePathBuilderNoneValueException
from storage.abc import FilePathBuilderABC


class SlugFilePathBuilder[TReadSchema](FilePathBuilderABC[TReadSchema]):
    def __init__(self, folder: str, field: str):
        self._folder = folder
        self._field = field

    def build(self, obj: TReadSchema) -> str:
        value = getattr(obj, self._field)
        if value is None:
            raise FilePathBuilderNoneValueException(field_name=self._field)
        return f"{self._folder}/{slugify(str(value))}"