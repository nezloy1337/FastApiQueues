from sqlalchemy import select

from domains.tags import Tags


async def test_create_tag(client, test_session):
    """Проверка, что POST / создаёт новый тег"""
    tag_data = {"name": "Test Tag"}

    response = client.post("/api_v1/tags", json=tag_data)

    assert response.status_code == 201
    assert response.json()["name"] == "Test Tag"

    # Проверяем, что объект действительно появился в БД
    query = select(Tags).filter(Tags.name == "Test Tag")
    result = await test_session.execute(query)
    assert result.scalar_one_or_none() is not None
