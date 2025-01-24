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



#нужен ли async
def handle_exception(func):
    """
      A decorator to handle exceptions during the execution of asynchronous functions.

      This decorator wraps the provided function and ensures that any exceptions raised
      during its execution are caught and passed to the `find_error_type` handler.

      :param func: The asynchronous function to be wrapped.
      :type func: Callable
      :return: A wrapped version of the provided function with exception handling.
      :rtype: Callable

      Example:
          >>> @handle_exception
          >>> async def my_function():
          >>>     # Your async logic here
          >>>     raise ValueError("An error occurred")

          When `my_function` is called, the raised exception will be handled by
          `find_error_type`.

      """
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
        Handles unexpected exceptions by logging, storing, and raising an HTTP 500 error.

        This function processes unhandled exceptions, logs the details, saves the error
        information to a database, and raises an HTTPException with a 500 status code.
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






