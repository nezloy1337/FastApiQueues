from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.api_v1.queues.schemas import CreateQueue
from core.models.queue import Queue


async def create_queue(
    session: AsyncSession,
    queue_to_create: CreateQueue,
):
    queue = Queue(**queue_to_create.model_dump())
    session.add(queue)
    await session.commit()
    return queue

async def get_queues(session: AsyncSession):
    result = await session.execute(select(Queue))
    queues = result.scalars().all()
    return queues
