from typing import Annotated

from fastapi import UploadFile, File


from constants import AllowedMimeTypes
from exceptions.files import UnsupportedMediaTypeException


def validate_image_file(file: Annotated[UploadFile, File(...)]):
    if file.content_type not in AllowedMimeTypes.get_values():
        raise UnsupportedMediaTypeException(
            current_type=file.content_type,
            allowed_types=AllowedMimeTypes.get_error_string()
        )
    return file