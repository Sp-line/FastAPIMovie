from app_types.log_level import LogLevel
from schemas.gunicorn import GunicornAppOptions


def get_app_options(
        host: str,
        port: int,
        timeout: int,
        workers: int,
        log_level: LogLevel,
) -> GunicornAppOptions:
    return GunicornAppOptions(
        host=host,
        port=port,
        timeout=timeout,
        workers=workers,
        loglevel=log_level,
    )
