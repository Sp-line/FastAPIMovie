import logging

from fastapi import FastAPI
from faststream.nats.fastapi import NatsRouter
from faststream.nats.opentelemetry import NatsTelemetryMiddleware

from core.config import settings
from telemetry.setup import get_tracer_provider

router = NatsRouter(
    str(settings.faststream.nats_url),
    middlewares=[NatsTelemetryMiddleware(tracer_provider=get_tracer_provider())] if settings.otlp.enabled else (),
)


@router.after_startup
async def configure_logging(app: FastAPI) -> None:
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.logging.log_format,
        datefmt=settings.logging.log_datefmt,
    )
