import logging
from datetime import datetime

from fastapi import HTTPException, status
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from core.models.mongodb import error_collection
from core.config import settings
from schemas.logging import ExceptionLogTemplate

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# обработчики частных ошибок
def handle_integrity_error(e: IntegrityError | HTTPException):
    logger.info(f"Ошибка целостности данных: { e.args }")

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=settings.errors_description.conflict_description,
    )


def handle_unexpected_error(e: Exception):
    """
    Обрабатывает непредвиденные ошибки, такие как отключение базы данных,
    и записывает их в MongoDB. Логируется информация об ошибке и время её возникновения.

    Параметры:
    e (Exception): Исключение, содержащее информацию об ошибке.

    Действия:
    1. Преобразует информацию об ошибке в строку.
    2. Записывает сообщение об ошибке в лог. (для удобства разработки)
    3. Создает экземпляр шаблона журнала ошибок с описанием ошибки и текущей временной меткой.
    4. Вставляет журнал ошибки в коллекцию MongoDB.
    5. Выбрасывает HTTP-исключение с кодом 500 и сообщением об неизвестной ошибке.
    """
    error_info = str(e)
    logger.info(f"Неизвестная ошибка: {error_info}")

    error_log = ExceptionLogTemplate(
        description=error_info,
        timestamp=datetime.now()
    )

    error_collection.insert_one(error_log.model_dump(exclude_none=True))

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
        #return чтобы не выполнялся дальше код если находится ошибка
        return handle_integrity_error(e)

    handle_unexpected_error(e)


def delete_queue_entry_handle_exception(e: Exception):
    if isinstance(e, HTTPException):
        if e.status_code == status.HTTP_404_NOT_FOUND:
            return handle_record_not_found(e)

    if isinstance(e, ValidationError):
        return handle_validation_error(e)

    handle_unexpected_error(e)


def average_handle_exception(e: Exception):

    if isinstance(e, ValidationError):
        return handle_validation_error(e)
    if isinstance(e, AttributeError):
        return handle_validation_error(e)
    if isinstance(e, IntegrityError):
        return handle_integrity_error(e)
    handle_unexpected_error(e)
