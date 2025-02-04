import inspect
from datetime import datetime, timezone
from functools import lru_cache, wraps
from typing import Callable

from pydantic import BaseModel

from core.base import Base
from core.mongodb.connection import CONNECTION_REGISTRY
from core.mongodb.schemas import ActionLog


@lru_cache
def get_signature(function):
    """
    Retrieves and caches the signature of the given function.
    """
    return inspect.signature(function)


def get_log_params(func, log_params, *args, **kwargs):
    """
    Extracts parameters for logging based on the function's signature
    and specified log parameters.

    Args:
        func (Callable[..., Any]): The function whose parameters are being extracted.
        log_params (List[str] | None): A list of parameter names to include in the log.
        args (Any): Positional arguments.
        kwargs (Any): Keyword arguments.

    Returns:
        Dict[str, Any]: A dictionary of extracted parameters.
    """

    log_params = log_params or []
    sig = get_signature(func)
    bound = sig.bind(*args, **kwargs)

    if not log_params:
        # Если log_params пуст, логируем все параметры
        return {
            name: value.model_dump() if isinstance(value, BaseModel | Base) else value
            for name, value in bound.arguments.items()
        }

    # Если log_params задан, фильтруем параметры
    return {
        name: value.model_dump() if isinstance(value, BaseModel | Base) else value
        for name, value in bound.arguments.items()
        if name in log_params
    }


# сделать async?
def log_action(
    action: str,
    collection_name: str,
    log_params: list[str] | None = None,
) -> Callable:
    """
    A decorator for logging actions to MongoDB.

    Args:
        action (str): A description or type of the action being logged.
        collection_name (str): The name of the MongoDB collection where logs are stored.
        log_params (List[str] | None, optional):
         A list of parameter names to include in the log.
        If None, all parameters are logged.

    Returns:
        Callable[[Callable[..., Any]], Callable[..., Any]]:
        A decorator that wraps the target function with logging functionality.

    Raises:
        ValueError: If the specified collection is not found in `CONNECTION_REGISTRY`.

    Example:
        >>> @log_action("create_user", "user_logs", ["username", "email"])
        >>> @router.post("")
        >>> async def create_user(username: str, email: str, password: str):
        >>>     pass
    """

    def decorator(func):
        logs_collection = CONNECTION_REGISTRY.get(collection_name)  # предзагрузка
        if logs_collection is None:
            raise ValueError(
                f"Collection '{collection_name}' not found in connection_registry."
            )

        @wraps(func)
        async def wrapper(*args, **kwargs):
            """
            Wrapper function that executes the decorated function and logs the action.

            Args:
                *args (Any): Positional arguments.
                **kwargs (Any): Keyword arguments.

            Returns:
                Any: The result of the decorated function.

            Raises:
                Exception: If the decorated function raises an exception.
            """

            status = "success"
            logged_args = get_log_params(func, log_params, *args, **kwargs)
            try:
                return await func(*args, **kwargs)

            except Exception as e:
                status = "failed"
                raise e

            finally:
                timestamp = datetime.now(timezone.utc)
                log_entry = ActionLog(
                    action=action,
                    parameters=logged_args,  # Только отфильтрованные параметры
                    status=status,
                    timestamp=timestamp,
                )

                await logs_collection.insert_one(log_entry.model_dump())

        return wrapper

    return decorator
