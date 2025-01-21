import inspect
from datetime import datetime, timezone
from functools import wraps, lru_cache
from typing import Optional, List, Callable

from pydantic import BaseModel

from core.mongodb.connection import CONNECTION_REGISTRY
from core.mongodb.schemas import ActionLog


@lru_cache
def get_signature(function):
    return inspect.signature(function)


def get_log_params(func, log_params, *args, **kwargs):

    log_params = log_params or []

    sig = get_signature(func)
    bound = sig.bind(*args, **kwargs)

    if not log_params:
        # Если log_params пуст, логируем все параметры
        return {
            name: value.model_dump() if isinstance(value, BaseModel) else value
            for name, value in bound.arguments.items()
        }

    # Если log_params задан, фильтруем параметры
    return {
        name: value.model_dump() if isinstance(value, BaseModel) else value
        for name, value in bound.arguments.items()
        if name in log_params
    }

#сделать async?
def log_action(
    action: str,
    collection_name: str,
    log_params: Optional[List[str]] = None,
) -> Callable:
    """
    Декоратор для логирования в MongoDB.

    :param action: Описание или тип действия (логически, что мы логируем).
    :param log_params: Список имён параметров функции, которые нужно залогировать.
                       Если None, логируются все параметры.
    :param collection_name: Имя коллекции в MongoDB, куда писать логи.
    """

    def decorator(func):
        logs_collection = CONNECTION_REGISTRY.get(collection_name) #предзагрузка
        if logs_collection is None:
            raise ValueError(f"Collection '{collection_name}' not found in connection_registry.")

        @wraps(func)
        async def wrapper(*args, **kwargs):
            status = "success"
            try:
                return await func(*args, **kwargs)

            except Exception as e:
                status = "failed"
                raise e

            finally:
                timestamp = datetime.now(timezone.utc)
                logged_args = get_log_params(func, log_params, *args, **kwargs)
                log_entry = ActionLog(
                    action=action,
                    parameters=logged_args,  # Только отфильтрованные параметры
                    status=status,
                    timestamp=timestamp,
                )


                await logs_collection.insert_one(log_entry.model_dump())

        return wrapper

    return decorator
