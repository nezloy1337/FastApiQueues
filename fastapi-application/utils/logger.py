from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable

from tasks import process_log


def get_log_params(log_params, **kwargs) -> dict[str, Any]:
    """
    Extracts and filters parameters for logging.

    If `log_params` is provided, only the specified parameters will be logged.
    If an object has a `model_dump` method (e.g., Pydantic models),
    its dumped representation is used.Otherwise, the raw value is returned.

    Args:
        log_params (tuple[str, ...] | None):
            A tuple of parameter names to include in the log.
            If `None`, all parameters are logged.
        kwargs (Any):
            Keyword arguments representing function parameters.

    Returns:
        dict[str, Any]:
            A dictionary of extracted parameters.

    Example:
        >>> params = get_log_params(("username"), username="JohnDoe", password="secret")
        >>> print(params)
        {"username": "JohnDoe",}
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
    A decorator for logging function executions to a MongoDB collection.

    This decorator extracts function parameters,
    and sends logs to a task queue.
    It ensures that failed executions
    are also logged with the error message.

    Args:
        action (str):
            A string describing the action being logged (e.g., `"create_user"`).
        collection_name (str):
            The name of the MongoDB collection where logs are stored.
        log_params (tuple[str, ...] | None, optional):
            A tuple of parameter names to include in the log.
            If `None`, all parameters are logged.

    Returns:
        Callable[[Callable[..., Any]], Callable[..., Any]]:
            A decorator that wraps the target function and logs its execution.


    Example:
        >>> @log_action("create_user", "user_logs", ("username", "email"))
        >>> @router.post("")
        >>> async def create_user(username: str, email: str, password: str):
        >>>     pass
    """

    def decorator(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            # fastapi always uses named args in endpoints
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
            error = None
            logged_args = get_log_params(log_params, **kwargs)

            try:
                return await func(*args, **kwargs)

            except Exception as e:
                status = "failed"
                error = str(e)
                raise e

            finally:
                timestamp = datetime.now(timezone.utc)
                data = {
                    "action": action,
                    "parameters": logged_args,
                    "status": status,
                    "timestamp": timestamp,
                    "collection_name": collection_name,
                }
                if error:
                    data.update({"error": error})

                process_log.apply_async(args=[data])

        return wrapper

    return decorator
