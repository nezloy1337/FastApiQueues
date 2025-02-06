from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable

from tasks import process_log

from core.mongodb.connection import CONNECTION_REGISTRY
from core.mongodb.schemas import ActionLog


def get_log_params(log_params, **kwargs) -> dict[str, Any]:
    """
    Extracts parameters for logging based on the function's signature
    and specified log parameters.

    Args:
        log_params (List[str] | None): A list of parameter names to include in the log.
        kwargs (Any): Keyword arguments.

    Returns:
        Dict[str, Any]: A dictionary of extracted parameters.
    """

    log_params = log_params or []

    if not log_params:
        return {
            name: value.model_dump() if hasattr(value, "model_dump") else value
            for name, value in kwargs.items()
        }

    # Если `log_params` задан, фильтруем параметры
    return {
        name: value.model_dump() if hasattr(value, "model_dump") else value
        for name, value in kwargs.items()
        if name in log_params
    }


def log_action(
    action: str,
    collection_name: str,
    log_params: tuple[str, ...] | None = None,
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
        async def wrapper(**kwargs):
            # fastapi всегда передает по имени
            """
            Wrapper function that executes the decorated function and logs the action.

            Args:
                **kwargs (Any): Keyword arguments.

            Returns:
                Any: The result of the decorated function.

            Raises:
                Exception: If the decorated function raises an exception.
            """

            status = "success"
            logged_args = get_log_params(log_params, **kwargs)

            try:
                return await func(**kwargs)
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

                data = log_entry.model_dump()
                process_log.apply_async(args=[data], queue="logs")

        return wrapper

    return decorator
