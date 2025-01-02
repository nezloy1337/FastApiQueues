from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.api_v1.queues.schemas import CreateQueue
from api.api_v1.queues_entries.schemas import QueueEntry
from core.models.queue import Queue,QueueEntries


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

async def get_queue_with_entries(session: AsyncSession, queue_id: int):
    query = (select(Queue)
            .join(Queue.entries)
            .join(QueueEntries.user)
            .where(Queue.id == queue_id)
            .options(selectinload(Queue.entries)
            .selectinload(QueueEntries.user)))
    result = await session.execute(query)
    queue_with_entries = result.scalars().first()
    return queue_with_entries
