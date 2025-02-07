import logging
from datetime import datetime
from unittest.mock import MagicMock

import pytest
from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from utils.logger import log_action


@pytest.mark.asyncio
async def test_log_action_success(
    patch_celery_apply_async: tuple[MagicMock, MagicMock]
) -> None:
    """
    Test log_action when the wrapped function succeeds.

    Verifies that when the function returns normally,
    the log data is sent via process_log.apply_async.
    """
    # Unpack the patched Celery mocks.
    mock_log_apply_async, _ = patch_celery_apply_async

    @log_action("TEST_ACTION", "test_collection", ("a",))
    async def dummy(a: int, b: int) -> int:
        return a + b

    # Call the decorated function.
    result = await dummy(a=1, b=2)
    assert result == 3

    # Ensure apply_async was called exactly once.
    mock_log_apply_async.assert_called_once()

    # Extract call arguments from the mock.
    # The decorator calls: process_log.apply_async(args=[log_data])
    args, kwargs = mock_log_apply_async.call_args
    data = kwargs["args"][0]

    # Verify that the log data is as expected.
    assert data["action"] == "TEST_ACTION"
    assert data["collection_name"] == "test_collection"
    # Only the allowed parameter "a" is logged.
    assert data["parameters"] == {"a": 1}
    assert data["status"] == "success"
    assert isinstance(data["timestamp"], datetime)
    assert "error" not in data


@pytest.mark.asyncio
async def test_log_action_failure(
    patch_celery_apply_async: tuple[MagicMock, MagicMock]
) -> None:
    """
    Test log_action when the wrapped function raises an exception.

    Verifies that if an error occurs, the log data contains
    the error message and the status is set to "failed".
    """
    mock_log_apply_async, _ = patch_celery_apply_async

    @log_action("FAIL_ACTION", "fail_collection", ("x", "y"))
    async def dummy_fail(x: int, y: int) -> None:
        raise ValueError("fail test")

    # Verify that the function raises the expected exception.
    with pytest.raises(ValueError) as excinfo:
        await dummy_fail(x=10, y=20)
    assert "fail test" in str(excinfo.value)

    # Ensure apply_async was called exactly once.
    mock_log_apply_async.assert_called_once()
    args, kwargs = mock_log_apply_async.call_args
    data = kwargs["args"][0]

    # Verify that the log data includes the error details.
    assert data["action"] == "FAIL_ACTION"
    assert data["collection_name"] == "fail_collection"

    # Allowed parameters "x" and "y" are logged.
    assert data["parameters"] == {"x": 10, "y": 20}
    assert data["status"] == "failed"
    assert data["error"] == "fail test"
    assert isinstance(data["timestamp"], datetime)


@pytest.mark.asyncio
async def test_apply_async_exception(
    patch_celery_apply_async: tuple[MagicMock, MagicMock],
    monkeypatch: MonkeyPatch,
    caplog: LogCaptureFixture,
) -> None:
    """
    Test log_action when process_log.apply_async raises an exception.

    Verifies that if apply_async fails, the error is caught and logged,
    but the wrapped function still returns its value.
    """
    mock_log_apply_async, _ = patch_celery_apply_async

    # Configure the mock to raise a RuntimeError when called.
    mock_log_apply_async.side_effect = RuntimeError("Celery down")

    # Set log capture for the 'process_log' logger at ERROR level.
    caplog.set_level(logging.ERROR, logger="process_log")

    @log_action("EXC_ACTION", "exc_collection")
    async def dummy(a: int) -> int:
        return a

    # Call the decorated function.
    result = await dummy(a=42)
    assert result == 42

    # Check that a log record with "Celery down" is present.
    found = any("Celery down" in record.message for record in caplog.records)
    assert found
