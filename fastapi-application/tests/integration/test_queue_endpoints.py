from datetime import date

import pytest
from sqlalchemy import select

from domains.queues import Queue


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "queue_data, result_code",
    [
        (
            {
                "name": "new-name",
                "start_time": "2025-02-03T11:30:19.650000Z",
                "max_slots": 25,
            },
            201,
        ),
        (
            {
                "name": 234,
                "start_time": "2025-02-03T11:30:19.650000Z",
                "max_slots": 25,
            },
            422,
        ),
        (
            {
                "name": "new-name",
                "start_time": "2023-02-03T11:30:19.650000Z",
                "max_slots": 22,
            },
            409,
        ),
        (
            {
                "name": "new-name",
                "start_time": "2023-02-03T11:30:19.650000Z",
                "max_slots": -1,
            },
            409,
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

    Test tag creation endpoint with various scenarios.
    Verifies proper status codes and database state changes.
    """
    response = client.post("/api_v1/queues", json=queue_data)

    # Validate response status code
    assert response.status_code == result_code

    if response.status_code == 201:
        # Verify response contains correct name
        assert response.json()["name"] == queue_data.get("name")

        # Check database persistence
        query = select(Queue).filter(Queue.name == queue_data.get("name"))
        result = await test_session.execute(query)
        assert result.scalar_one_or_none() is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "queue_data, expected_status",
    [
        (
            {
                "name": "updated-name",
                "start_time": "2026-02-03T11:30:19.650000Z",
                "max_slots": 30,
            },
            200,  # Успешное обновление
        ),
        (
            {
                "name": 1234,  # Некорректный тип имени
                "start_time": "2025-02-03T11:30:19.650000Z",
                "max_slots": 25,
            },
            422,  # Ошибка валидации
        ),
        (
            {
                "name": "updated-name",
                "start_time": "2023-02-03T11:30:19.650000Z",  # Прошедшая дата
                "max_slots": 22,
            },
            409,  # Конфликт из-за некорректной даты
        ),
        (
            {
                "name": "updated-name",
                "start_time": "2025-02-03T11:30:19.650000Z",
                "max_slots": -5,  # Некорректное число слотов
            },
            409,  # Конфликт из-за некорректного количества слотов
        ),
    ],
)
async def test_update_queue(
    client,
    test_session,
    test_queue: Queue,  # Фикстура для получения существующей очереди
    queue_data: dict[str, str | date | int],
    expected_status: int,
):
    """
    Тест для обновления очереди с различными вариантами входных данных.
    Проверяет корректность статуса ответа и изменения в базе данных.
    """
    queue_id = test_queue.id  # Используем ID очереди из фикстуры

    # Отправляем PUT-запрос на обновление очереди
    response = client.put(f"/api_v1/queues/{queue_id}", json=queue_data)

    # Проверяем статус ответа
    assert response.status_code == expected_status

    if response.status_code == 200:
        # Проверяем, что данные обновились корректно
        assert response.json()["name"] == queue_data.get("name")

        # Проверяем, что изменения сохранились в базе данных
        query = select(Queue).filter(Queue.id == queue_id)
        result = await test_session.execute(query)
        updated_queue = result.scalar_one_or_none()

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
        (None, 204),  # Successful deletion (uses fixture-created tag ID)
        (999, 404),  # Non-existent tag ID
        ("invalid", 422),  # Malformed tag ID
    ],
)
async def test_delete_queue(
    client,
    test_session,
    test_queue: Queue,  # Fixture provides tag for deletion test case
    queue_id: int,
    expected_status: int,
):
    """
    Test tag deletion endpoint with various ID scenarios.
    Verifies proper database state changes after operations.
    """
    # Use fixture-generated ID for successful deletion case
    if queue_id is None:
        queue_id = test_queue.id

    # Send DELETE request
    response = client.delete(f"/api_v1/queues/{queue_id}")

    # Validate response status code
    assert response.status_code == expected_status

    if expected_status == 204:
        # Confirm record removal from database
        db_tag = await test_session.get(Queue, queue_id)
        assert db_tag is None
