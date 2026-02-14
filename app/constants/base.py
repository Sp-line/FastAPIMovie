from enum import StrEnum
from functools import lru_cache


class ImageUrlLimits:
    MAX: int = 1024
    MIN: int = 1


class AllowedMimeTypes(StrEnum):
    JPEG = "image/jpeg"
    PNG = "image/png"
    WEBP = "image/webp"

    @classmethod
    @lru_cache
    def get_values(cls) -> list[str]:
        return [member.value for member in cls]

    @classmethod
    @lru_cache
    def get_error_string(cls) -> str:
        return ", ".join(cls.get_values())