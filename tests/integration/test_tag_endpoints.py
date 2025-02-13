import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domains.tags import Tags


@pytest_asyncio.fixture(scope="function")
async def test_tag(test_session: AsyncSession) -> Tags:
    """
    Creates 2 test tags.

    Yields:
        Tags: A test tag instance.
    """
    tag = Tags(name="test-tag")
    tag2 = Tags(name="test-tag-2")
    test_session.add(tag)
    test_session.add(tag2)
    await test_session.commit()
    await test_session.refresh(tag)
    return tag


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tag_data, result_code",
    [
        # Case 1: Valid tag creation
        ({"name": "new-name"}, 201),
        # Case 2: Invalid name type (should be a string)
        ({"name": 12345}, 422),
        # Case 3: Duplicate tag name, should return conflict
        ({"name": "test-tag-2"}, 409),
        # Case 4: Invalid field in request body
        ({"invalid_field": "value"}, 422),
    ],
)
async def test_create_tag(
    client,
    test_session,
    test_tag,
    tag_data: dict[str, str],
    result_code: int,
) -> None:
    """
    Test the tag creation API endpoint.

    This test verifies:
    - That a valid tag can be created successfully (201).
    - That invalid data (wrong field types or duplicate entries)
      is rejected with the expected status.
    - That created tags persist in the database.

    Args:
        client (TestClient): The FastAPI test client.
        test_session (AsyncSession): The database session.
        test_tag (Tags): The test tag fixture.
        tag_data (dict): Data for the tag creation request.
        result_code (int): Expected HTTP response status.
    """

    # Send POST request to create a tag
    response = client.post("/api_v1/tags", json=tag_data)

    # Validate response status code
    assert response.status_code == result_code

    if response.status_code == 201:
        # Ensure the response contains the correct name
        assert response.json()["name"] == tag_data.get("name")

        # Verify the tag was successfully stored in the database
        query = select(Tags).filter(Tags.name == tag_data.get("name"))
        result = await test_session.execute(query)
        assert result.scalar_one_or_none() is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_data, expected_status",
    [
        # Case 1: Valid tag update
        ({"name": "new-name"}, 200),
        # Case 2: Invalid name type (should be a string)
        ({"name": 12345}, 422),
        # Case 3: Duplicate tag name, should return conflict
        ({"name": "test-tag-2"}, 409),
        # Case 4: Invalid field in request body
        ({"invalid_field": "value"}, 422),
    ],
)
async def test_update_tag(
    client: TestClient,
    test_session: AsyncSession,
    test_tag: Tags,
    update_data: dict[str, str],
    expected_status: int,
) -> None:
    """
    Test the tag update API endpoint.

    This test verifies:
    - That a valid tag update request is processed correctly.
    - That invalid updates (wrong field types or duplicate names) are rejected.
    - That successful updates reflect correctly in the database.

    Args:
        client (TestClient): The FastAPI test client.
        test_session (AsyncSession): The database session.
        test_tag (Tags): The test tag fixture.
        update_data (dict): Data for updating the tag.
        expected_status (int): Expected HTTP response status.
    """

    # Send PATCH request to update the tag
    response = client.patch(f"/api_v1/tags/{test_tag.id}", json=update_data)

    # Validate response status code
    assert response.status_code == expected_status

    if expected_status == 200:
        # Ensure the response contains the updated name
        data = response.json()
        assert data["name"] == update_data["name"]

        # Refresh the database entity and verify changes
        await test_session.refresh(test_tag)
        assert test_tag.name == update_data["name"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tag_id, expected_status",
    [
        (None, 204),  # Case 1: Valid tag ID, should be deleted successfully
        (999, 404),  # Case 2: Non-existent tag ID, should return not found
        (
            "invalid",
            422,
        ),  # Case 3: Invalid tag ID format, should return validation error
    ],
)
async def test_delete_tag(
    client: TestClient,
    test_session: AsyncSession,
    test_tag: Tags,
    tag_id: int | str,
    expected_status: int,
) -> None:
    """
    Test the tag deletion API endpoint.

    This test verifies:
    - That an existing tag can be deleted successfully (204).
    - That attempting to delete a non-existent tag returns 404.
    - That passing an invalid tag_id format returns a validation error (422).

    Args:
        client (TestClient): The FastAPI test client.
        test_session (AsyncSession): The database session.
        test_tag (Tags): The test tag fixture.
        tag_id (Union[int, str]): The tag ID to be deleted.
        expected_status (int): Expected HTTP response status.
    """

    # Use test tag ID if None is passed
    if tag_id is None:
        tag_id = test_tag.id

    # Send DELETE request to remove the tag
    response = client.delete(f"/api_v1/tags/{tag_id}")

    # Validate response status code
    assert response.status_code == expected_status

    if expected_status == 204:
        # Ensure the tag was actually deleted from the database
        deleted_tag = await test_session.get(Tags, tag_id)
        assert deleted_tag is None
