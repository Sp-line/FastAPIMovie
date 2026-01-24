from fastapi import Request, status, FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError

from exceptions.db import ObjectNotFoundException, UniqueFieldException, UniqueException, \
    RelatedObjectNotFoundException, DeleteConstraintException


def register_db_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ObjectNotFoundException)
    async def object_not_found_handler(request: Request, exc: ObjectNotFoundException) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "object_id": exc.id_repr,
                "table_name": exc.table_name,
                "detail": str(exc),
            },
        )

    @app.exception_handler(UniqueFieldException)
    async def unique_field_handler(request: Request, exc: UniqueFieldException) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "field_name": exc.field_name,
                "table_name": exc.table_name,
                "detail": str(exc)
            },
        )

    @app.exception_handler(UniqueException)
    async def unique_handler(request: Request, exc: UniqueException) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "fields": ", ".join(exc.fields),
                "table_name": exc.table_name,
                "detail": str(exc)
            },
        )

    @app.exception_handler(RelatedObjectNotFoundException)
    async def related_object_not_found_handler(request: Request, exc: RelatedObjectNotFoundException) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "field_name": exc.field_name,
                "table_name": exc.table_name,
                "detail": str(exc)
            },
        )

    @app.exception_handler(DeleteConstraintException)
    async def delete_constraint_handler(request: Request, exc: DeleteConstraintException) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "table_name": exc.table_name,
                "referencing_table": exc.referencing_table,
                "detail": str(exc)
            },
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError) -> ORJSONResponse:
        error_detail = str(exc.orig) if hasattr(exc, "orig") else str(exc)
        error_detail = error_detail.replace("\n", " ").strip()

        return ORJSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": "Database integrity error",
                "debug_message": error_detail,
            },
        )
