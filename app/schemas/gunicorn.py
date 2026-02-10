from typing import Annotated

from gunicorn.glogging import Logger
from pydantic import Field, BaseModel, computed_field, ConfigDict

from log import LogLevel
from core.gunicorn.logger import GunicornLogger


class GunicornAppOptions(BaseModel):
    timeout: Annotated[int, Field(ge=0)] = 900
    workers: Annotated[int, Field(ge=1)] = 1
    loglevel: LogLevel = "info"

    accesslog: str = "-"
    errorlog: str = "-"
    worker_class: str = "uvicorn.workers.UvicornWorker"
    logger_class: type[Logger] = GunicornLogger

    bind: str = "0.0.0.0:8000"

    model_config = ConfigDict(arbitrary_types_allowed=True)
