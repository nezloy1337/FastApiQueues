import logging
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DBAPIError, IntegrityError

from core.mongodb import error_collection
from core.mongodb.schemas import ExceptionLogTemplate
from utils.exceptions import DuplicateEntryError

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):
    """Registers custom exception handlers for the FastAPI application."""

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Handles validation errors for incorrect value types"""
        return JSONResponse(
            status_code=400,
            content={
                "error": "Validation Error",
                "message": str(exc),
            },
        )

    @app.exception_handler(AttributeError)
    async def handle_attr_error(request: Request, exc: AttributeError) -> JSONResponse:
        """Handles missing or incorrect attribute access"""
        return JSONResponse(
            status_code=400,  # 400 Bad Request
            content={
                "error": "Attribute Error",
                "message": str(exc),
            },
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        """Handles database integrity constraint violations"""
        return JSONResponse(
            status_code=409,  # 409 Conflict
            content={
                "error": "Database Conflict (IntegrityError)",
                "message": str(exc),
            },
        )

    @app.exception_handler(DuplicateEntryError)
    async def duplicate_entry_error_handler(request: Request, exc: DuplicateEntryError):
        """Handles duplicate entry attempts in unique constrained fields"""
        return JSONResponse(
            status_code=409,  # 409 Conflict
            content={
                "error": "Duplicate Entry (IntegrityError)",
                "message": "Resource already exists with these parameters",
            },
        )

    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        """Handles standard HTTP exceptions"""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "API Error",
                "message": exc.detail,
            },
        )

    @app.exception_handler(DBAPIError)
    async def dbapi_error_handler(request: Request, exc: DBAPIError):
        """Handles low-level database API errors"""
        return JSONResponse(
            status_code=400,  # 400 Bad Request
            content={
                "error": "Database Operation Failed",
                "message": "Database constraint violation detected",
            },
        )

    @app.exception_handler(OSError)
    async def ose_error_handler(request: Request, exc: OSError):
        """Handles operating system related errors"""
        return JSONResponse(
            status_code=500,  # 500 Internal Server Error
            content={
                "error": "System Error",
                "message": "Internal server operation failed",
            },
        )

    @app.exception_handler(Exception)
    async def unknown_error_handler(request: Request, exc: Exception):
        """Fallback handler for uncaught exceptions"""
        error_info = str(exc)
        error_log = ExceptionLogTemplate(
            description=error_info,
            timestamp=datetime.now(),
        )

        try:
            await error_collection.insert_one(error_log.model_dump(exclude_none=True))
        except Exception as e:
            raise e

        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": str(exc),
            },
        )
