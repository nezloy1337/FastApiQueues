import logging
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from core.mongodb import error_collection
from core.mongodb.schemas import ExceptionLogTemplate
from utils.exceptions import DuplicateEntryError

# Настройка логирования
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):
    """Регистрация обработчиков исключений"""

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):

        return JSONResponse(
            status_code=400,
            content={"error": "ValueError", "message": str(exc)},
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=409,  # Код 409 (Conflict) — конфликт данных в БД
            content={
                "error": "IntegrityError",
                "message": str(exc),
            },
        )

    @app.exception_handler(DuplicateEntryError)
    async def duplicate_entry_error_handler(request: Request, exc: DuplicateEntryError):
        return JSONResponse(
            status_code=409,  # Код 409 (Conflict) — конфликт данных в БД
            content={
                "error": "IntegrityError",
                "message": "У вас уже есть место в очереди",
            },
        )

    @app.exception_handler(AttributeError)
    async def handle_attr_error(request: Request, exc: AttributeError) -> JSONResponse:
        return JSONResponse(
            status_code=400,  # Код 400 (Bad Request) — Ошибка получения атрибута
            content={
                "error": "AttributeError",
                "message": str(exc),
            },
        )

    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": str(exc)},
        )

    @app.exception_handler(OSError)
    async def ose_error_handler(request: Request, exc: OSError):
        error_info = str(exc)
        error_log = ExceptionLogTemplate(
            description=error_info,
            timestamp=datetime.now(),
        )

        await error_collection.insert_one(error_log.model_dump(exclude_none=True))
        return JSONResponse(status_code=500, content={"error": error_info})

    @app.exception_handler(Exception)
    async def unknown_error_handler(request: Request, exc: Exception):
        error_info = str(exc)
        error_log = ExceptionLogTemplate(
            description=error_info,
            timestamp=datetime.now(),
        )

        await error_collection.insert_one(error_log.model_dump(exclude_none=True))
        return JSONResponse(status_code=500, content={"error": error_info})
