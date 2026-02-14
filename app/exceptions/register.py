from fastapi import FastAPI

from exceptions.db_handlers import register_db_exception_handlers
from exceptions.elastic_handlers import register_elastic_exception_handlers
from exceptions.files_handlers import register_files_exception_handlers
from exceptions.redis_handlers import register_redis_exception_handlers
from exceptions.s3_handlers import register_s3_exception_handlers


def register_exception_handlers(app: FastAPI) -> None:
    register_db_exception_handlers(app)
    register_s3_exception_handlers(app)
    register_redis_exception_handlers(app)
    register_elastic_exception_handlers(app)
    register_files_exception_handlers(app)
