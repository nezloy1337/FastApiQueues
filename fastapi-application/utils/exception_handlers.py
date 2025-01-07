import logging
from datetime import datetime

from fastapi import HTTPException, status
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from core.models.mongodb import error_collection

from core.config import settings

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#преобразование массива в строку
array_to_str = lambda args: ', '.join(map(str, args))

# обработчики частных ошибок
def handle_integrity_error(e: IntegrityError | HTTPException):
    logger.info(f"Ошибка целостности данных: { e.args }")
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=settings.errors_description.conflict_description,
    )


def handle_unknown_error(e: Exception):
    error_description = array_to_str(e.args)
    logger.info(f"неизвестная ошибка: { error_description }")
    error_collection.insert_one(
        {
            "type": "unknown_error",
            "description": f"{e.args}",
            "time":datetime.now(),
        }
    )
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=settings.errors_description.unknown_error_description,
    )


def handle_record_not_found(e: HTTPException):
    logger.info(f"запись в базе данных не найдена: { e.args }")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=settings.errors_description.no_entry_description,
    )


def handle_validation_error(e: ValidationError):
    logger.info(f"ошибка валидации данных:{ e.args }")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=settings.errors_description.validation_error_description,
    )


# обработчики ошибок функций
# для каждой очереди отдельно для более тонкой настройки
def create_queue_entry_handle_exception(e: Exception):
    if isinstance(e, IntegrityError):
        handle_integrity_error(e)
    if isinstance(e, Exception):
        handle_unknown_error(e)


def delete_queue_entry_handle_exception(e: Exception):
    if isinstance(e, HTTPException):
        if e.status_code == status.HTTP_404_NOT_FOUND:
            handle_record_not_found(e)
            return
    if isinstance(e, ValidationError):
        handle_validation_error(e)
        return
    handle_unknown_error(e)


def average_handle_exception(e: Exception):
    handle_unknown_error(e)
