import logging
from datetime import datetime
from typing import Callable

from core.mongodb import error_collection
from core.mongodb.schemas import ExceptionLogTemplate
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette import status

# Настройка логирования
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


# нужен ли async
def handle_exception(func) -> Callable:
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

        except IntegrityError as exception:
            handle_integrity_error(exception)
        except ValidationError as exception:
            handle_validation_error(exception)
        except HTTPException as exception:
            raise exception
        except AttributeError as exception:
            handle_attr_error(exception)
        except Exception as exception:
            # Ловим все остальные исключения для логирования и обработки
            await handle_unexpected_error(exception)

    return wrapper


def handle_validation_error(e: ValidationError) -> None:
    logger.error(f"ошибка валидации данных:{ e.args }")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="ошибка валидации данных",
    )


def handle_integrity_error(e: IntegrityError) -> None:
    logger.error(f"Ошибка целостности данных: { str(e) }")

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="ошибка целостности данных",
    )


def handle_attr_error(e: AttributeError) -> None:
    logger.error(f"ошибка получения атрибута: {str(e)}")

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="ошибка получения атрибута",
    )


async def handle_unexpected_error(e: Exception) -> None:
    """
    Handles unexpected exceptions by logging, storing, and raising an HTTP 500 error.

    This function processes unhandled exceptions, logs the details, saves the error
    information to a database, and raises an HTTPException with a 500 status code.
    """

    error_info = str(e)
    logger.info(f"Неизвестная ошибка: {error_info}")

    error_log = ExceptionLogTemplate(description=error_info, timestamp=datetime.now())

    await error_collection.insert_one(error_log.model_dump(exclude_none=True))

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="unknown error occurred ",
    )
