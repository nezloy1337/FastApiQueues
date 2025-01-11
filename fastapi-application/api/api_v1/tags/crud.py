from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.tags.schemas import CreateTag, CreateTagQueue
from core.models import User, Tags, QueueTags


async def create_tag(tag_to_create: CreateTag, user: User, session: AsyncSession):
    tag = Tags(**tag_to_create.model_dump())
    session.add(tag)
    await session.commit()
    return tag


async def create_tag_queue(
    tag_queue_to_create: CreateTagQueue,
    user: User,
    session: AsyncSession,
):
    queue_tag = QueueTags(**tag_queue_to_create.model_dump())
    session.add(queue_tag)
    await session.commit()
    return queue_tag

async def get_tags(session: AsyncSession):
    query = select(Tags)
    result = await session.execute(query)
    return result.scalars().all()

