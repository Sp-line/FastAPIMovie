from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

from exceptions.files import UnsupportedMediaTypeException


def register_files_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UnsupportedMediaTypeException)
    async def unsupported_media_type_handler(request: Request, exc: UnsupportedMediaTypeException):
        return ORJSONResponse(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            content={
                "allowed_types": exc.allowed_types,
                "current_type": exc.current_type,
                "detail": str(exc),
            },
        )