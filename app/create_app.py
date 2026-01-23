from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.models import db_helper
from storage.s3 import s3_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await s3_helper.connect()

    yield

    # shutdown
    await s3_helper.close()
    await db_helper.dispose()


def create() -> FastAPI:
    app = FastAPI(
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    return app
