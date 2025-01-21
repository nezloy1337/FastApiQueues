import inspect
from datetime import datetime
from functools import wraps
from typing import Optional, List, Callable

from pydantic import BaseModel

from core.mongodb.connection import CONNECTION_REGISTRY
from core.mongodb.schemas import ActionLog


def log_action(
    action: str, log_params: Optional[List[str]] = None, collection_name: str = "logs"
) -> Callable:
    """
    Декоратор для логирования в MongoDB.

    :param action: Описание или тип действия (логически, что мы логируем).
    :param log_params: Список имён параметров функции, которые нужно залогировать.
                       Если None, логируются все параметры.
    :param collection_name: Имя коллекции в MongoDB, куда писать логи.
    """
    if log_params is None:
        log_params = []

    def decorator(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            status = "success"
            try:
                return await func(*args, **kwargs)

            except Exception as e:
                status = "failed"
                raise

            finally:
                timestamp = datetime.now()
                sig = inspect.signature(func)
                bound = sig.bind(*args, **kwargs)

                logged_args = {}

                for name,value in bound.arguments.items():
                    if name in log_params:
                        if isinstance(value, BaseModel):
                            logged_args[name] = value.model_dump()
                        else:
                            logged_args[name] = value

                log_entry = ActionLog(
                    action=action,
                    parameters=logged_args,  # Только отфильтрованные параметры
                    status=status,
                    timestamp=timestamp
                )
                # log_entry = {
                #     "action": action,
                #     "parameters": logged_args,  # Только отфильтрованные параметры
                #     "status": status,
                #     "timestamp": str(timestamp),
                # }

                logs_collection = CONNECTION_REGISTRY.get(collection_name)
                await logs_collection.insert_one(log_entry.model_dump())

        return wrapper

    return decorator
