from fastapi import HTTPException,status
from sqlalchemy import select
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


async def clear_queues_entry(
    session: AsyncSession,
):
    try:
        result = await session.execute(select(QueueEntries))
        to_delete = result.scalars().all()
        for record in to_delete:
            await session.delete(record)
        await session.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
