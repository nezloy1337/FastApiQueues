import logging
from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable

from tasks import process_log


def get_log_params(
    allowed_params: tuple[str, ...] | None,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Filter kwargs by allowed_params.

    If allowed_params is None or empty, return all kwargs.
    For values with a model_dump method, return its dump.
    """

    allowed_params = allowed_params or []

    if allowed_params:
        return {
            name: value.model_dump() if hasattr(value, "model_dump") else value
            for name, value in kwargs.items()
            if name in allowed_params
        }

    return {
        name: value.model_dump() if hasattr(value, "model_dump") else value
        for name, value in kwargs.items()
    }


def log_action(
    action: str,
    collection_name: str,
    log_params: tuple[str, ...] | None = None,
) -> Callable:
    """
    A decorator for logging FastApi endpoint params to a MongoDB collection.

    Logs the action, parameters of the endpoint, status, and timestamp.
    If an error occurs, the error is logged too.

    Args:
        action (str):
            A string describing the action being logged (e.g., `"POST"`).
        collection_name (str):
            The name of the MongoDB collection where logs are stored.
        log_params (tuple[str, ...] | None, optional):
            A tuple of parameter names to include in the log.
            If `None`, all parameters are logged.

    Example:
        >>> @router.post("")
        >>> @log_action("create_user", "user_logs", ("username", "email"))
        >>> async def create_user(username: str, email: str, password: str):
        >>>     pass

    """

    def decorator(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            # fastapi always uses named args in endpoints
            """
            Wrapper function that executes the decorated function and logs the action.
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
                try:
                    process_log.apply_async(args=[data])
                except Exception as e:
                    # must crete a method that saves log to postgres if rabbitmq is down
                    log = logging.getLogger("process_log")
                    log.exception("error occurred while executing process_log %s", e)

        return wrapper

    return decorator
