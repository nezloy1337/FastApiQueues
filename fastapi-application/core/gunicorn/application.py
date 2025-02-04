# type: ignore
from typing import Any

from fastapi import FastAPI
from gunicorn.app.base import BaseApplication


class Application(BaseApplication):
    """
    Custom Gunicorn application wrapper for integrating FastAPI with Gunicorn.

    This class allows running a FastAPI application
    with Gunicorn while managing configuration dynamically.
    """

    def __init__(
        self,
        app: FastAPI,
        options: dict[str, Any],
    ):
        """
        Initializes the custom Gunicorn application
        with a FastAPI instance and configuration options.

        Args:
            app (FastAPI): The FastAPI application instance.
            options (Dict[str, Any]): Configuration options for Gunicorn.
        """
        self.options = options or {}
        self.application = app
        super().__init__()

    def load(self) -> FastAPI:
        """
        Returns the FastAPI application instance.

        Returns:
            FastAPI: The FastAPI app to be run by Gunicorn.
        """
        return self.application

    @property
    def config_options(self) -> dict[str, Any]:
        """
        Filters and returns the configuration options that are valid for Gunicorn.

        Returns:
            Dict[str, Any]: A dictionary of configuration options supported by Gunicorn.
        """
        return {k: v for k, v in self.options.items() if k in self.cfg.settings}

    def load_config(self) -> None:
        """
        Loads the filtered configuration options into Gunicorn settings.
        """
        for key, value in self.config_options.items():
            self.cfg.set(key.lower(), value)
