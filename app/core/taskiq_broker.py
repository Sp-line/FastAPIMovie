import logging

import taskiq_fastapi
from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker

from core.config import settings

log = logging.getLogger(__name__)

broker = AioPikaBroker(
    uri=str(settings.taskiq.url),
)

taskiq_fastapi.init(broker, "main:main_app")


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_worker_startup(state: TaskiqState) -> None:
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.taskiq.log_format,
        datefmt=settings.logging.log_datefmt,
    )
    log.info(f"Worker startup complete, got state: %s", state)
