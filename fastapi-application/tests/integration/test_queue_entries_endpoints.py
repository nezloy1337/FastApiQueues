import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from domains.queues import Queue
from domains.queues.models import QueueEntries


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "queue_entry_data, result_code",
    [
        # Case 1: Valid queue entry with an automatically assigned queue_id
        (
            {
                "position": 2,
                "queue_id": None,  # This will be assigned in the test
            },
            201,  # Expected success response
        ),
        # Case 2: Position exceeds allowed limits, should result in conflict
        (
            {
                "position": 999,
                "queue_id": None,  # This will be assigned in the test
            },
            409,  # Expected conflict response
        ),
    ],
)
async def test_create_queue_entry(
    client: TestClient,
    test_session: AsyncSession,
    test_queue: Queue,
    patch_celery_apply_async,
    queue_entry_data: dict[str, int],
    result_code: int,
) -> None:
    """
    Test the queue entry creation API endpoint.

    This test verifies:
    - That a queue entry can be created with valid input.
    - That an entry with an invalid position results in a conflict (409).
    - That created entries persist in the database.

    Args:
        client (TestClient): The FastAPI test client.
        test_session (AsyncSession): The database session.
        test_queue (Queue): The test queue fixture.
        queue_entry_data (dict): Data for the queue entry request.
        result_code (int): Expected HTTP response status.
    """
    mock_log_apply_async, mock_error_apply_async = patch_celery_apply_async
    # Assign queue_id dynamically if it is None
    if queue_entry_data["queue_id"] is None:
        queue_entry_data["queue_id"] = test_queue.id

    # Send POST request to create a queue entry
    response = client.post("/api_v1/queue", json=queue_entry_data)

    # Validate response status code
    assert response.status_code == result_code

    if response.status_code == 201:
        mock_log_apply_async.assert_called_once()
        mock_error_apply_async.assert_not_called()
        # Verify that the response contains the correct queue_id
        assert response.json()["queue_id"] == queue_entry_data.get("queue_id")

        # Ensure the entry was successfully stored in the database
        query = select(QueueEntries).filter(
            QueueEntries.queue_id == queue_entry_data.get("queue_id"),
            QueueEntries.position == queue_entry_data.get("position"),
        )
        result = await test_session.execute(query)
        assert result.scalar_one_or_none() is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "queue_id, result_code",
    [
        (1, 204),  # Case 1: Valid queue_id, should delete successfully
        (999, 404),  # Case 2: Non-existent queue_id, should return not found
        (
            "invalid",
            422,
        ),  # Case 3: Invalid queue_id format, should return validation error
    ],
)
async def test_delete_queue_entry(
    client: TestClient,
    test_session: AsyncSession,
    test_queue: Queue,
    patch_celery_apply_async,
    result_code: int,
    test_queue_entry: QueueEntries,
    queue_id: int,
) -> None:
    """
    Test the queue entry deletion API endpoint.

    This test verifies:
    - That an existing queue entry can be deleted successfully (204).
    - That attempting to delete a non-existent entry returns 404.
    - That passing an invalid queue_id format returns a validation error (422).

    Args:
        client (TestClient): The FastAPI test client.
        test_session (AsyncSession): The database session.
        test_queue_entry (QueueEntries): The test queue entry fixture.
        queue_id (Union[int, str]): The queue_id to be deleted.
        result_code (int): Expected HTTP response status.
    """
    mock_log_apply_async, mock_error_apply_async = patch_celery_apply_async
    # Send DELETE request to remove the queue entry
    response = client.delete(f"/api_v1/queue/{queue_id}")

    # Validate response status code
    assert response.status_code == result_code

    if response.status_code == 204:
        mock_log_apply_async.assert_called_once()
        mock_error_apply_async.assert_not_called()
        # Ensure the entry was actually deleted from the database
        deleted_obj = await test_session.get(QueueEntries, test_queue_entry.id)
        assert deleted_obj is None
