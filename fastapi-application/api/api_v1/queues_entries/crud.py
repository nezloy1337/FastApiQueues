from sqlalchemy.ext.asyncio import AsyncSession
from api.api_v1.queues_entries.schemas import QueueEntry
from core.models import QueueEntries


async def create_queues_entry(
    session: AsyncSession,
    queue_entry_to_create: QueueEntry,
):
    queue_entry = QueueEntries(**queue_entry_to_create.model_dump())
    session.add(queue_entry)
    await session.commit()
    return queue_entry


async def get_queues_entries():
    pass


async def delete_queues_entry(
    queue_entry_id: int,
    session: AsyncSession,
):
    pass
