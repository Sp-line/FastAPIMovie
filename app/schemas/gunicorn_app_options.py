from typing import Annotated

from gunicorn.glogging import Logger
from pydantic import Field, BaseModel, computed_field

from app_types.log_level import LogLevel
from core.gunicorn.logger import GunicornLogger


class GunicornAppOptions(BaseModel):
    host: str = "0.0.0.0"
    port: Annotated[int, Field(ge=1, le=65535)] = 8000
    timeout: Annotated[int, Field(ge=0)] = 900
    workers: Annotated[int, Field(ge=1)] = 1
    loglevel: LogLevel = "info"

    accesslog: str = "-"
    errorlog: str = "-"
    worker_class: str = "uvicorn.workers.UvicornWorker"
    logger_class: Logger = GunicornLogger

    @computed_field
    @property
    def bind(self) -> str:
        return f"{self.host}:{self.port}"
