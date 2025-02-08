from typing import Any
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from fastapi import HTTPException

from core.base import BaseService


@pytest_asyncio.fixture
def base_service(mock_repository: AsyncMock) -> BaseService[Any, AsyncMock]:
    """
    Provides an instance of `BaseService` with a mocked repository.
    """
    return BaseService(mock_repository)


@pytest_asyncio.fixture
def mock_repository() -> AsyncMock:
    """
    Provides a mocked repository with async methods for unit testing.
    """
    repo = AsyncMock()
    repo.create = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.get_all = AsyncMock()
    repo.delete = AsyncMock()
    repo.patch = AsyncMock()
    return repo


@pytest.mark.asyncio
async def test_get_by_id_not_found(
    base_service,
    mock_repository,
) -> None:
    """
    Tests the `get_by_id` method when the object is not found.
    It should raise an HTTP 404 exception.
    """
    obj_id = 1
    mock_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await base_service.get_by_id(obj_id)

    mock_repository.get_by_id.assert_awaited_once_with(obj_id)
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_delete_success(
    base_service,
    mock_repository,
) -> None:
    """
    Tests the `delete` method to ensure an object is deleted successfully.
    """
    filters = {"id": 1}
    mock_repository.delete.return_value = True

    result = await base_service.delete(filters)

    mock_repository.delete.assert_awaited_once_with(**filters)
    assert result is True


@pytest.mark.asyncio
async def test_delete_not_found(
    base_service,
    mock_repository,
):
    """
    Tests the `delete` method when the object is not found.
    It should raise an HTTP 404 exception.
    """
    filters = {"id": 1}
    mock_repository.delete.return_value = False

    with pytest.raises(HTTPException) as exc_info:
        await base_service.delete(filters)

    mock_repository.delete.assert_awaited_once_with(**filters)
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_patch_not_found(
    base_service,
    mock_repository,
) -> None:
    """
    Tests the `patch` method when the object is not found.
    It should raise an HTTP 404 exception.
    """
    filters = {"id": 1}
    update_values = {"name": "Updated Name"}
    mock_repository.patch.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await base_service.patch(filters, **update_values)

    mock_repository.patch.assert_awaited_once_with(filters, **update_values)
    assert exc_info.value.status_code == 404
