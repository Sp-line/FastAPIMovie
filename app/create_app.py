from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core import broker, fs_router
from core.models import db_helper
from exceptions.register import register_exception_handlers
from storage.s3 import s3_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    await s3_helper.connect()

    if not broker.is_worker_process:
        await broker.startup()

    yield

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
