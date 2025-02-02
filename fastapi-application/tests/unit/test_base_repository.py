from unittest.mock import Mock

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

    obj = await repo.create(obj_data)

    for key, value in obj_data.items():
        assert getattr(obj, key) == value

    mock_session.add.assert_called_once_with(obj)  # Проверяем вызов add()
    mock_session.commit.assert_called_once()  # Проверяем вызов commit()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model_class, obj_id",
    [
        (Tags, 1),
        (QueueTags, 2),
    ],
)
async def test_get_by_id(mock_session, mock_condition_builder, model_class, obj_id):
    """Проверяем, что create() вызывает session.add() и commit()."""
    repo = BaseRepository(model_class, mock_session, mock_condition_builder)

    await repo.get_by_id(obj_id)
    mock_session.get.assert_called_once_with(
        model_class, obj_id
    )  # Проверяем вызов get()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model_class, mock_result",
    [
        (Tags, [Tags(name="Tag1"), Tags(name="Tag2")]),
        (QueueTags, [QueueTags(queue_id=1, tag_id=1)]),
        (Tags, []),
    ],
)
async def test_get_all(mock_session, mock_condition_builder, model_class, mock_result):
    """Проверяем, что get_all() возвращает все объекты модели."""
    repo = BaseRepository(model_class, mock_session, mock_condition_builder)

    # Мокируем результат execute
    mock_scalars = Mock()
    mock_scalars.all.return_value = mock_result
    mock_session.execute.return_value = Mock(scalars=Mock(return_value=mock_scalars))

    result = await repo.get_all()

    # Проверяем вызов execute с правильным запросом
    assert isinstance(result, list)
    assert result == mock_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "deleted_obj, should_commit",
    [
        (Tags(id=1, name="Deleted Tag"), True),  # Объект найден
        (None, False),  # Объект не найден
    ],
)
async def test_delete_commits_only_on_success(
    mock_session, mock_condition_builder, deleted_obj, should_commit
):
    model_class = Tags
    conditions = {"id": 1}

    # Мокируем condition_builder и результат удаления
    mock_condition_builder.create_conditions.return_value = [model_class.id == 1]
    mock_session.execute.return_value = Mock(
        scalar_one_or_none=Mock(return_value=deleted_obj)
    )

    repo = BaseRepository(model_class, mock_session, mock_condition_builder)
    result = await repo.delete(**conditions)

    # Проверяем возврат удаленного объекта
    assert result == deleted_obj

    # Проверяем вызов commit()
    if should_commit:
        mock_session.commit.assert_called_once()
    else:
        mock_session.commit.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "updated_obj, should_commit",
    [
        (Tags(id=1, name="New Name"), True),  # Обновление успешно
        (None, False),  # Объект не найден
    ],
)
async def test_patch_updates_fields_and_commits(
    mock_session, mock_condition_builder, updated_obj, should_commit
):
    model_class = Tags
    filters = {"id": 1}
    update_values = {"name": "New Name"}

    # Мокируем condition_builder и результат обновления
    mock_condition_builder.create_conditions.return_value = [model_class.id == 1]
    mock_session.execute.return_value = Mock(
        scalar_one_or_none=Mock(return_value=updated_obj)
    )

    repo = BaseRepository(model_class, mock_session, mock_condition_builder)
    result = await repo.patch(filters, **update_values)

    # Проверяем возврат обновленного объекта
    assert result == updated_obj

    # Проверяем вызов commit()
    if should_commit:
        mock_session.commit.assert_called_once()
    else:
        mock_session.commit.assert_not_called()
