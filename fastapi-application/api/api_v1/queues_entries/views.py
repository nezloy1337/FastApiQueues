from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from api.api_v1.queues_entries.schemas import CreateQueueEntry
from core.models import db_helper


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
    queue_in: CreateQueueEntry,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    queue_id,
):
    return {"af": 23}


# @router.get(
#     "/queue/{queue_id}",
# )
# async def create_queue(
#     queue_in: CreateQueue,
#     session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
# ):
#     return await crud.create_queue(session, queue_in)
