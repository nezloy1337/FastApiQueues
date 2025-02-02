import pytest
from sqlalchemy import select

from domains.tags import Tags


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tag_data, result_code",
    [
        ({"name": "new-name"}, 201),  # Successful name update
        ({"name": 12345}, 422),  # Invalid type for name field
        ({"name": "test-tag-2"}, 409),  # Conflict with existing tag name
        ({"invalid_field": "value"}, 422),  # Non-existent field update attempt
    ],
)
async def test_create_tag(
    client,
    test_session,
    test_tag,  # Fixture creates base test-tag entry for conflict testing
    tag_data: dict[str, str],
    result_code: int,
):
    """
    Test tag creation endpoint with various scenarios.
    Verifies proper status codes and database state changes.
    """
    # Send POST request to create tag
    response = client.post("/api_v1/tags", json=tag_data)

    # Validate response status code
    assert response.status_code == result_code

    if response.status_code == 201:
        # Verify response contains correct name
        assert response.json()["name"] == tag_data.get("name")

        # Check database persistence
        query = select(Tags).filter(Tags.name == tag_data.get("name"))
        result = await test_session.execute(query)
        assert result.scalar_one_or_none() is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_data, expected_status",
    [
        ({"name": "new-name"}, 200),  # Successful name update
        ({"name": 12345}, 422),  # Invalid type for name field
        ({"name": "test-tag-2"}, 409),  # Conflict with existing tag name
        ({"invalid_field": "value"}, 422),  # Non-existent field update attempt
    ],
)
async def test_update_tag(
    client,
    test_session,
    test_tag: Tags,  # Fixture provides existing tag to modify
    update_data: dict,
    expected_status: int,
):
    """
    Test tag update endpoint functionality.
    Covers successful updates, validation errors, and conflict cases.
    """
    # Send PATCH request to update tag
    response = client.patch(f"/api_v1/tags/{test_tag.id}", json=update_data)

    # Verify expected HTTP status
    assert response.status_code == expected_status

    if expected_status == 200:
        # Validate response data matches update
        data = response.json()
        assert data["name"] == update_data["name"]

        # Verify database record was updated
        await test_session.refresh(test_tag)
        assert test_tag.name == update_data["name"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tag_id, expected_status",
    [
        (None, 204),  # Successful deletion (uses fixture-created tag ID)
        (999, 404),  # Non-existent tag ID
        ("invalid", 422),  # Malformed tag ID
    ],
)
async def test_delete_tag(
    client,
    test_session,
    test_tag: Tags,  # Fixture provides tag for deletion test case
    tag_id: int | str,
    expected_status: int,
):
    """
    Test tag deletion endpoint with various ID scenarios.
    Verifies proper database state changes after operations.
    """
    # Use fixture-generated ID for successful deletion case
    if tag_id is None:
        tag_id = test_tag.id

    # Send DELETE request
    response = client.delete(f"/api_v1/tags/{tag_id}")

    # Validate response status code
    assert response.status_code == expected_status

    if expected_status == 204:
        # Confirm record removal from database
        db_tag = await test_session.get(Tags, tag_id)
        assert db_tag is None
