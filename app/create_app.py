from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import event_handlers  # noqa: F401
from cache import redis_helper
from core import broker, fs_router
from core.models import db_helper
from elastic.elasticsearch import es_helper
from exceptions.register import register_exception_handlers
from storage.s3 import s3_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    await s3_helper.connect()
    if not broker.is_worker_process:
        await broker.startup()
    await redis_helper.connect()
    await es_helper.connect()
    await es_helper.documents_init()

    yield

    await es_helper.close()
    await redis_helper.close()
    if not broker.is_worker_process:
        await broker.shutdown()

    await s3_helper.close()
    await db_helper.dispose()


def create() -> FastAPI:
    app = FastAPI(
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    app.include_router(fs_router)
    register_exception_handlers(app)
    return app
