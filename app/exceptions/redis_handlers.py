from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

from exceptions.redis import RedisClientNotInitializedException


def register_redis_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RedisClientNotInitializedException)
    async def redis_client_config_handler(request: Request, exc: RedisClientNotInitializedException):
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)},
        )
