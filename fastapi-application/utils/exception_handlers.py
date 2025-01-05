import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from core.config import settings

# Настройка логирования
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


# обработчики частных ошибок
def handle_integrity_error(e: IntegrityError | HTTPException):
    logger.error(f"Ошибка целостности данных: {e.args}")
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=settings.errors_description.conflict_description,
    )


def handle_unknown_error(e: Exception):
    logger.error(f"неизвестная ошибка: {e.args}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=settings.errors_description.unknown_error_description,
    )


def handle_record_not_found(e: HTTPException):
    logger.error(f"запись в базе данных не найдена: {e.args}")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=settings.errors_description.no_entry_description,
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
    handle_unknown_error(e)

def average_handle_exception(e: Exception):
    handle_unknown_error(e)
