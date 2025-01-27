from core.config import settings
from core.gunicorn import Application, get_app_options
from main import main_app


def main() -> None:
    app = Application(
        app=main_app,
        options=get_app_options(
            host=settings.gunicorn.host,
            port=settings.gunicorn.port,
            workers=settings.gunicorn.workers,
            timeout=settings.gunicorn.timeout,
        ),
    )
    app.run()


if __name__ == "__main__":
    main()
