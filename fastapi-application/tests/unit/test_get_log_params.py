from typing import Any
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from pydantic import BaseModel

from utils.logger import get_log_params


class MockPydanticModel(BaseModel):
    """A mock class that simulates a Pydantic model."""

    name: str
    age: int


# Create a mock instance of MockPydanticModel
mock_pydantic_model = MockPydanticModel(name="Alice", age=30)

# Generate a unique user ID
user_id = uuid4()

# Create a mock user object
mock_user = MagicMock()
mock_user.id = user_id
mock_user.last_name = "User"
mock_user.first_name = "Test"
mock_user.model_dump.return_value = {
    "id": mock_user.id,
    "first_name": mock_user.first_name,
    "last_name": mock_user.last_name,
}


@pytest.mark.parametrize(
    "log_params, kwargs, expected_output",
    [
        # ✅ Test 1: Log all parameters (log_params=None)
        (
            None,
            {
                "param1": "hello",
                "param2": 42,
                "param3": mock_pydantic_model,
                "param4": mock_user,
            },
            {
                "param1": "hello",
                "param2": 42,
                "param3": {"name": "Alice", "age": 30},
                "param4": {
                    "id": user_id,
                    "first_name": "Test",
                    "last_name": "User",
                },
            },
        ),
        # Test 2: Filter only "param1"
        (
            "param1",
            {
                "param1": "hello",
                "param2": 42,
                "param3": mock_pydantic_model,
                "param4": mock_user,
            },
            {
                "param1": "hello",
            },
        ),
        # Test 3: Filter "param1" and "param2"
        (
            ("param1", "param2"),
            {
                "param1": "hello",
                "param2": 42,
                "param3": mock_pydantic_model,
                "param4": mock_user,
            },
            {
                "param1": "hello",
                "param2": 42,
            },
        ),
    ],
)
def test_get_log_params(
    log_params: Any,
    kwargs: dict[str, Any],
    expected_output: dict[str, Any],
):
    """
    Test to ensure correct extraction and filtering of parameters.

    Args:
        log_params (Any): A tuple or string containing parameter names to filter,
        or None to log all parameters.
        kwargs (dict[str, Any]): A dictionary containing function arguments.
        expected_output (dict[str, Any]): The expected output.

    Raises:
        AssertionError: If the actual output does not match the expected output.
    """
    result = get_log_params(log_params, **kwargs)
    assert result == expected_output, f"Expected {expected_output}, but got {result}"
