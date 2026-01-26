from fastapi import Request, status, FastAPI
from fastapi.responses import ORJSONResponse

from exceptions.s3 import S3ClientNotInitializedException, S3UploadException, S3DeleteException, \
    FilePathBuilderNoneValueException


def register_s3_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(S3ClientNotInitializedException)
    async def s3_client_config_handler(request: Request, exc: S3ClientNotInitializedException):
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)},
        )

    @app.exception_handler(S3UploadException)
    async def s3_upload_handler(request: Request, exc: S3UploadException):
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "object_name": exc.obj_name,
                "detail": str(exc)
            },
        )

    @app.exception_handler(S3DeleteException)
    async def s3_delete_handler(request: Request, exc: S3DeleteException):
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "object_name": exc.obj_name,
                "detail": str(exc)
            },
        )

    @app.exception_handler(FilePathBuilderNoneValueException)
    async def file_path_builder_none_value(request: Request, exc: FilePathBuilderNoneValueException):
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "field_name": exc.field_name,
                "detail": str(exc)
            },
        )
