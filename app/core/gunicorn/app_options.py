from core.gunicorn.logger import GunicornLogger


def get_app_options(
        host: str,
        port: int,
        timeout: int,
        workers: int,
        log_level: str,
) -> dict:
    return {
        "accesslog": "-",
        "errorlog": "-",
        "bind": f"{host}:{port}",
        "workers": workers,
        "timeout": timeout,
        "logger_class": GunicornLogger,
        "loglevel": log_level,
        "worker_class": "uvicorn.workers.UvicornWorker",
    }
