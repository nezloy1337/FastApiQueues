from unittest.mock import AsyncMock

import pytest

from core.base import BaseRepository
from domains.queues import QueueTags
from domains.tags import Tags


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model_class, obj_data",
    [
        (  # Тест для Tag
            Tags,
            {
                "name": "Test Tag",
            },
        ),
        (  # Тест для QueueTags
            QueueTags,
            {
                "queue_id": 2,
                "tag_id": 2,
            },
        ),
    ],
)
async def test_create(mock_session, mock_condition_builder, model_class, obj_data):
    """Проверяем, что create() вызывает session.add() и commit()."""
    repo = BaseRepository(model_class, mock_session, mock_condition_builder)

    mock_session.commit = AsyncMock()

    obj = await repo.create(obj_data)

    for key, value in obj_data.items():
        assert getattr(obj, key) == value

    mock_session.add.assert_called_once_with(obj)  # Проверяем вызов add()
    mock_session.commit.assert_called_once()  # Проверяем вызов commit()
