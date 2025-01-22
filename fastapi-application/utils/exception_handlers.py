import logging
from datetime import datetime

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette import status

from core.config import settings
from core.mongodb import error_collection
from core.mongodb.schemas import ExceptionLogTemplate

# Настройка логирования
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def handle_exception(func):

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as exception:

            find_error_type(exception)

    return wrapper

def find_error_type(exception):
    match exception:

        case IntegrityError():
            return handle_integrity_error(exception)
        case ValidationError():
            return handle_validation_error(exception)
        case HTTPException():
            raise
        case AttributeError():
            raise

    return handle_unexpected_error(exception)

# обработчики частных ошибок
def handle_validation_error(e: ValidationError):
    logger.error(f"ошибка валидации данных:{ e.args }")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="ошибка валидации данных",
    )


def handle_integrity_error(e: IntegrityError):
    logger.error(f"Ошибка целостности данных: { str(e) }")

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="ошибка целостности данных",
    )

def handle_attr_error(e: AttributeError):
    logger.error(f"ошибка получения атрибута: {str(e)}")

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="ошибка получения атрибута",
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






