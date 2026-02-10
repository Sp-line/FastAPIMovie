from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator, metrics

from core.config import settings


def setup_metrics(app: FastAPI):
    if not settings.metrics.enabled:
        return

    instrumentator = Instrumentator(
        excluded_handlers=[
            "/metrics",
            "/docs",
            "/redoc",
            "/favicon.ico",
            "/asyncapi",
        ],
    )

    instrumentator.instrument(app).expose(app, endpoint=settings.metrics.endpoint)