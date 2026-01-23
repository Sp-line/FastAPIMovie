from typing import Any

from fastapi import FastAPI
from gunicorn.app.base import BaseApplication


class Application(BaseApplication):
    def __init__(self, app: FastAPI, options: dict):
        self.options = options
        self.app = app
        super().__init__()

    @property
    def config_options(self) -> dict[str, Any]:
        return {
            k: v
            for k, v in self.options.items()
            if k in self.cfg.settings and v is not None
        }

    def load_config(self) -> None:
        for key, value in self.config_options.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> FastAPI:
        return self.app