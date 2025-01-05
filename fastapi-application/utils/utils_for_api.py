from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

from core.config import settings

# Настройка логирования
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def create_queue_entry_handle_exception(e: Exception):
    if isinstance(e, IntegrityError):
        logger.error(f"Ошибка целостности данных: {e.args}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=settings.errors_description.conflict_description
        )
    else:
        logger.error(f"Неизвестная ошибка: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=settings.errors_description.unknown_error_description)
