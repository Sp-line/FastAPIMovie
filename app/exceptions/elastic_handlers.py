from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

from exceptions.elastic import ElasticClientNotInitializedException, ElasticConnectionFailed


def register_elastic_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ElasticClientNotInitializedException)
    async def elastic_client_config_handler(request: Request, exc: ElasticClientNotInitializedException):
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ElasticConnectionFailed)
    async def elastic_connection_failed(request: Request, exc: ElasticConnectionFailed):
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)},
        )
