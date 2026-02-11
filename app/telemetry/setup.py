from functools import lru_cache

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.elasticsearch import ElasticsearchInstrumentor
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from sqlalchemy.ext.asyncio import AsyncEngine
from taskiq.instrumentation import TaskiqInstrumentor

from core.config import settings


@lru_cache(maxsize=1)
def get_tracer_provider() -> TracerProvider:
    resource = Resource.create(attributes={
        "service.name": settings.otlp.service_name,
    })
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=settings.otlp.endpoint, insecure=True)
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    return provider


def setup_telemetry(app: FastAPI, engine: AsyncEngine) -> None:
    provider = get_tracer_provider()

    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
    SQLAlchemyInstrumentor().instrument(
        engine=engine.sync_engine,
        enable_commenter=True,
        tracer_provider=provider,
    )
    RedisInstrumentor().instrument(tracer_provider=provider)
    ElasticsearchInstrumentor().instrument()
    AioHttpClientInstrumentor().instrument()
    TaskiqInstrumentor().instrument()
    LoggingInstrumentor().instrument(set_logging_format=True)
