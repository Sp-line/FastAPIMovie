import logging

import taskiq_fastapi
from taskiq import TaskiqEvents, TaskiqState, TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker

from .config import settings

log = logging.getLogger(__name__)

broker = AioPikaBroker(
    url=str(settings.taskiq.url),
)
scheduler = TaskiqScheduler(broker, sources=[LabelScheduleSource(broker)])

taskiq_fastapi.init(broker, "main:main_app")


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_worker_startup(state: TaskiqState) -> None:
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.taskiq.log_format,
        datefmt=settings.logging.log_datefmt,
    )
    log.info(f"Worker startup complete, got state: %s", state)
