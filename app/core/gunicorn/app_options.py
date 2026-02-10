from log import LogLevel
from schemas.gunicorn import GunicornAppOptions


def get_app_options(
        host: str,
        port: int,
        timeout: int,
        workers: int,
        log_level: LogLevel,
) -> GunicornAppOptions:
    return GunicornAppOptions(
        bind=f"{host}:{port}",
        timeout=timeout,
        workers=workers,
        loglevel=log_level,
    )
