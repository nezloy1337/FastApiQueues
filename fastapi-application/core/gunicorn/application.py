# type: ignore
from fastapi import FastAPI
from gunicorn.app.base import BaseApplication


class Application(BaseApplication):
    def __init__(
        self,
        app: FastAPI,
        options: dict,
    ):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load(self) -> FastAPI:
        return self.application

    @property
    def config_options(self):
        return {k: v for k, v in self.options.items() if k in self.cfg.settings}

    def load_config(self) -> None:
        for key, value in self.config_options.items():
            self.cfg.set(key.lower(), value)
