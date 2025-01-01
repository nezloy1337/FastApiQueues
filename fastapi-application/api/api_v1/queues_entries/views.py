from typing import Annotated
from fastapi import APIRouter, HTTPException
from fastapi import Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from api.api_v1.queues_entries.crud import create_queues_entry
from api.api_v1.queues_entries.schemas import CreateQueueEntry, QueueEntry
from core.models import db_helper

from core.models import QueueEntries


router = APIRouter(
    prefix="",
    tags=["queues_entries"],
)


@router.post(
    "/queue/{queue_id}",
    response_model=CreateQueueEntry,
    status_code=status.HTTP_200_OK,
)
async def create_queue_entry(
    queue_entry_to_create: CreateQueueEntry,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],

):
    return await create_queues_entry(session,queue_entry_to_create)





@router.get(
    "/queue/{queue_id}",
    response_model=QueueEntry,
)
async def get_queue_entry(
    queue_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    pass




@router.delete(
    "/queue/{queue_id}",
)
async def delete_queue_entry(
    queue_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    try:
        result = await session.execute(select(QueueEntries))
        to_delete = result.scalars().all()
        await session.delete(to_delete[0])
        await session.commit()
        return {23:24}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
