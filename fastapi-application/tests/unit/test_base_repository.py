from unittest.mock import Mock

import pytest

from core.base import BaseRepository
from domains.queues import QueueTags
from domains.tags import Tags


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model_class, obj_data",
    [
        # Case 1: Creating a Tag object
        (
            Tags,
            {"name": "Test Tag"},
        ),
        # Case 2: Creating a QueueTag object
        (
            QueueTags,
            {"queue_id": 2, "tag_id": 2},
        ),
    ],
)
async def test_create(mock_session, mock_condition_builder, model_class, obj_data):
    """
    Test object creation via the repository.

    This test verifies:
    - That an object is correctly created with the given data.
    - That the created object has all expected attributes.
    - That the database session's `add` and `commit` methods are called once.

    Args:
        mock_session (AsyncMock): Mocked async database session.
        mock_condition_builder (MagicMock): Mocked condition builder.
        model_class (Type[Base]): The database model class.
        obj_data (dict): The data used to create the object.
    """

    repo = BaseRepository(model_class, mock_session, mock_condition_builder)
    obj = await repo.create(obj_data)

    # Validate that object attributes match input data
    for key, value in obj_data.items():
        assert getattr(obj, key) == value

    # Ensure the object was added and committed in the session
    mock_session.add.assert_called_once_with(obj)
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model_class, obj_id",
    [
        (Tags, 1),  # Case 1: Fetching a Tag by ID
        (QueueTags, 2),  # Case 2: Fetching a QueueTag by ID
    ],
)
async def test_get_by_id(mock_session, mock_condition_builder, model_class, obj_id):
    """
    Test fetching an object by ID.

    This test ensures:
    - That the correct model and ID are passed to `session.get`.

    Args:
        mock_session (AsyncMock): Mocked async database session.
        mock_condition_builder (MagicMock): Mocked condition builder.
        model_class (Type[Base]): The database model class.
        obj_id (int): The object ID to retrieve.
    """

    repo = BaseRepository(model_class, mock_session, mock_condition_builder)
    await repo.get_by_id(obj_id)

    # Ensure session.get() was called with the correct model and ID
    mock_session.get.assert_called_once_with(model_class, obj_id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model_class, mock_result",
    [
        # Case 1: Fetching multiple Tags
        (Tags, [Tags(name="Tag1"), Tags(name="Tag2")]),
        # Case 2: Fetching QueueTags with one entry
        (QueueTags, [QueueTags(queue_id=1, tag_id=1)]),
        # Case 3: Fetching an empty list (no records found)
        (Tags, []),
    ],
)
async def test_get_all(mock_session, mock_condition_builder, model_class, mock_result):
    """
    Test fetching all objects of a model.

    This test ensures:
    - That the repository correctly retrieves all objects from the database.
    - That the expected list of objects is returned.

    Args:
        mock_session (AsyncMock): Mocked async database session.
        mock_condition_builder (MagicMock): Mocked condition builder.
        model_class (Type[Base]): The database model class.
        mock_result (list): The expected query result.
    """

    repo = BaseRepository(model_class, mock_session, mock_condition_builder)

    # Mock the session.execute() behavior to return the expected results
    mock_scalars = Mock()
    mock_scalars.all.return_value = mock_result
    mock_session.execute.return_value = Mock(scalars=Mock(return_value=mock_scalars))

    result = await repo.get_all()

    # Ensure the returned result matches the expected output
    assert isinstance(result, list)
    assert result == mock_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "deleted_obj, should_commit",
    [
        # Case 1: Object exists and should be deleted
        (Tags(id=1, name="Deleted Tag"), True),
        # Case 2: No object found, so no commit should happen
        (None, False),
    ],
)
async def test_delete_commits_only_on_success(
    mock_session, mock_condition_builder, deleted_obj, should_commit
):
    """
    Test deleting an object.

    This test ensures:
    - That if the object exists, it is deleted and committed.
    - That if the object does not exist, the transaction is not committed.

    Args:
        mock_session (AsyncMock): Mocked async database session.
        mock_condition_builder (MagicMock): Mocked condition builder.
        deleted_obj (Optional[Base]): The object to delete, or None if not found.
        should_commit (bool): Whether the session should commit after deletion.
    """

    model_class = Tags
    conditions = {"id": 1}

    # Mock condition builder and database response
    mock_condition_builder.create_conditions.return_value = [model_class.id == 1]
    mock_session.execute.return_value = Mock(
        scalar_one_or_none=Mock(return_value=deleted_obj)
    )

    repo = BaseRepository(model_class, mock_session, mock_condition_builder)
    result = await repo.delete(**conditions)

    # Ensure the returned result matches the expected deleted object
    assert result == deleted_obj

    # Validate commit behavior
    if should_commit:
        mock_session.commit.assert_called_once()
    else:
        mock_session.commit.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "updated_obj, should_commit",
    [
        # Case 1: Object is updated and committed
        (Tags(id=1, name="New Name"), True),
        # Case 2: No object found, so no commit should happen
        (None, False),
    ],
)
async def test_patch_updates_fields_and_commits(
    mock_session, mock_condition_builder, updated_obj, should_commit
):
    """
    Test updating fields in an object.

    This test ensures:
    - That if an object is found, its fields are updated and committed.
    - That if no object is found, no commit occurs.

    Args:
        mock_session (AsyncMock): Mocked async database session.
        mock_condition_builder (MagicMock): Mocked condition builder.
        updated_obj (Optional[Base]): The updated object, or None if not found.
        should_commit (bool): Whether the session should commit after updating.
    """

    model_class = Tags
    filters = {"id": 1}
    update_values = {"name": "New Name"}

    # Mock condition builder and database response
    mock_condition_builder.create_conditions.return_value = [model_class.id == 1]
    mock_session.execute.return_value = Mock(
        scalar_one_or_none=Mock(return_value=updated_obj)
    )

    repo = BaseRepository(model_class, mock_session, mock_condition_builder)
    result = await repo.patch(filters, **update_values)

    # Ensure the returned result matches the expected updated object
    assert result == updated_obj

    # Validate commit behavior
    if should_commit:
        mock_session.commit.assert_called_once()
    else:
        mock_session.commit.assert_not_called()
