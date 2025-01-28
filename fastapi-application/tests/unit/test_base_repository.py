import datetime

import pytest

from core.base import BaseRepository
from domains.queues import Queue


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_data, expected_name",
    [
        (
            {
                "name": "string",
                "start_time": datetime.date(2025, 1, 1),
                "max_slots": 30,
            },
            "string",
        ),
    ],
)
async def test_create(test_session, mock_condition_builder, input_data, expected_name):
    repo = BaseRepository(Queue, test_session, mock_condition_builder)

    obj = await repo.create(input_data)

    assert obj.name == expected_name
    assert obj.id is not None

    # Проверяем в базе
    result = await test_session.get(Queue, obj.id)
    assert result is not None
    assert result.name == expected_name
