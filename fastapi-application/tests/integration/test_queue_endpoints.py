from datetime import date

import pytest
from sqlalchemy import select

from domains.queues import Queue


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "queue_data, result_code",
    [
        # Case 1: Valid queue creation with a future start time
        (
            {
                "name": "new-name",
                "start_time": "3030-02-03T11:30:19.650000Z",
                "max_slots": 25,
            },
            201,  # Expected success response
        ),
        # Case 2: Invalid name type (should be a string)
        (
            {
                "name": 234,  # Invalid name type
                "start_time": "2025-02-03T11:30:19.650000Z",
                "max_slots": 25,
            },
            422,  # Expected validation error
        ),
        # Case 3: Start time is in the past, should trigger conflict
        (
            {
                "name": "new-name",
                "start_time": "2023-02-03T11:30:19.650000Z",
                "max_slots": 22,
            },
            409,  # Expected conflict response
        ),
        # Case 4: Negative max_slots, which is not allowed
        (
            {
                "name": "new-name",
                "start_time": "2023-02-03T11:30:19.650000Z",
                "max_slots": -1,
            },
            409,  # Expected conflict response
        ),
    ],
)
async def test_create_queue(
    client,
    test_session,
    test_queue,
    queue_data: dict[str, str | date | int],
    result_code: int,
):
    """
    Test the queue creation API endpoint.

    This test verifies:
    - That valid data results in a successful queue creation (201).
    - That invalid data, such as incorrect types or past dates,
      returns the expected errors.
    - That created queues persist in the database.

    Args:
        client (TestClient): The FastAPI test client.
        test_session (AsyncSession): The database session.
        test_queue (Queue): The test queue fixture.
        queue_data (dict): Data for the queue creation request.
        result_code (int): Expected HTTP response status.
    """

    # Send POST request to create a queue
    response = client.post("/api_v1/queues", json=queue_data)

    # Validate response status code
    assert response.status_code == result_code

    if response.status_code == 201:
        # Ensure the response contains the correct name
        assert response.json()["name"] == queue_data.get("name")

        # Verify the queue was successfully stored in the database
        query = select(Queue).filter(Queue.name == queue_data.get("name"))
        result = await test_session.execute(query)
        assert result.scalar_one_or_none() is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "queue_data, expected_status",
    [
        # Case 1: Valid update
        (
            {
                "name": "updated-name",
                "start_time": "2026-02-03T11:30:19.650000Z",
                "max_slots": 30,
            },
            200,  # Expected successful update
        ),
        # Case 2: Invalid name type (should be a string)
        (
            {
                "name": 1234,  # Invalid name type
                "start_time": "2025-02-03T11:30:19.650000Z",
                "max_slots": 25,
            },
            422,  # Expected validation error
        ),
        # Case 3: Start time is in the past, should trigger conflict
        (
            {
                "name": "updated-name",
                "start_time": "2023-02-03T11:30:19.650000Z",
                "max_slots": 22,
            },
            409,  # Expected conflict response
        ),
        # Case 4: Negative max_slots, which is not allowed
        (
            {
                "name": "updated-name",
                "start_time": "2025-02-03T11:30:19.650000Z",
                "max_slots": -5,
            },
            409,  # Expected conflict response
        ),
    ],
)
async def test_update_queue(
    client,
    test_session,
    test_queue: Queue,
    queue_data: dict[str, str | date | int],
    expected_status: int,
):
    """
    Test the queue update API endpoint.

    This test verifies:
    - That valid updates are applied correctly.
    - That invalid updates (e.g., incorrect data types or past dates) are rejected.
    - That the database reflects the correct updated values after a successful update.

    Args:
        client (TestClient): The FastAPI test client.
        test_session (AsyncSession): The database session.
        test_queue (Queue): The test queue fixture.
        queue_data (dict): Data for updating the queue.
        expected_status (int): Expected HTTP response status.
    """

    queue_id = test_queue.id

    # Send PUT request to update the queue
    response = client.put(f"/api_v1/queues/{queue_id}", json=queue_data)

    # Validate response status code
    assert response.status_code == expected_status

    if response.status_code == 200:
        # Ensure the response contains the correct updated name
        assert response.json()["name"] == queue_data.get("name")

        # Retrieve the updated queue from the database
        query = select(Queue).filter(Queue.id == queue_id)
        result = await test_session.execute(query)
        updated_queue = result.scalar_one_or_none()

        # Validate that the update was correctly applied
        assert updated_queue is not None
        assert updated_queue.name == queue_data.get("name")
        assert updated_queue.start_time.isoformat().replace(
            "+00:00", "Z"
        ) == queue_data.get("start_time")
        assert updated_queue.max_slots == queue_data.get("max_slots")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "queue_id, expected_status",
    [
        (None, 204),  # Case 1: Valid queue ID, should be deleted successfully
        (999, 404),  # Case 2: Non-existent queue ID, should return not found
        (
            "invalid",
            422,
        ),  # Case 3: Invalid queue ID format, should return validation error
    ],
)
async def test_delete_queue(
    client,
    test_session,
    test_queue: Queue,
    queue_id: int,
    expected_status: int,
):
    """
    Test the queue deletion API endpoint.

    This test verifies:
    - That an existing queue can be deleted successfully (204).
    - That attempting to delete a non-existent queue returns 404.
    - That passing an invalid queue_id format returns a validation error (422).

    Args:
        client (TestClient): The FastAPI test client.
        test_session (AsyncSession): The database session.
        test_queue (Queue): The test queue fixture.
        queue_id (Union[int, str]): The queue ID to be deleted.
        expected_status (int): Expected HTTP response status.
    """

    # Use test queue ID if None is passed
    if queue_id is None:
        queue_id = test_queue.id

    # Send DELETE request to remove the queue
    response = client.delete(f"/api_v1/queues/{queue_id}")

    # Validate response status code
    assert response.status_code == expected_status

    if expected_status == 204:
        # Ensure the queue was actually deleted from the database
        deleted_queue = await test_session.get(Queue, queue_id)
        assert deleted_queue is None
