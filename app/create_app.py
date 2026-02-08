from contextlib import asynccontextmanager

from dishka import make_async_container
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import event_handlers  # noqa: F401
from cache import redis_helper
from core import broker, fs_router
from core.models import db_helper
from dependencies.infrastructure import InfrastructureProvider
from dependencies.repositories import RepositoryProvider
from dependencies.services import ServiceProvider
from elastic.elasticsearch import es_helper
from exceptions.register import register_exception_handlers

from dishka.integrations.fastapi import setup_dishka as setup_fastapi_dishka
from dishka.integrations.faststream import setup_dishka as setup_faststream_dishka
from dishka.integrations.taskiq import setup_dishka as setup_taskiq_dishka

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

    container = make_async_container(
        InfrastructureProvider(),
        RepositoryProvider(),
        ServiceProvider(),
    )

    setup_fastapi_dishka(container, app)
    setup_taskiq_dishka(container, broker)
    setup_faststream_dishka(container, broker=fs_router.broker, auto_inject=True)

    app.include_router(fs_router)
    register_exception_handlers(app)
    return app
